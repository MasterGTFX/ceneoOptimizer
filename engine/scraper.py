import requests
from bs4 import BeautifulSoup
from offer_scraper import TableScraper
import logging

logging.basicConfig(level=logging.DEBUG, filename='logs/app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(asctime)s %(message)s')
logger = logging.getLogger(__name__)


class WrongPageException(BaseException):
    pass


class CeneoScraper:
    RETRY_NUMBER = 5

    @staticmethod
    def create_url(product_name, min_price, max_price):
        """
        :param str product_name:         Product to be searched
        :return:                        Url for ceneo search to a given product
        """
        return "https://www.ceneo.pl/szukaj-" + product_name + ";m" + str(min_price) + ";n" + str(max_price) + ";0112-0"

    def get_products(self, url, **kwargs):
        """

        :param str url:     Link to search result page for given product name
        :return:            List containing products href
        """
        all_products_page = BeautifulSoup(requests.get(url).text, 'html.parser')
        products = [product for product in
                    all_products_page.find_all(class_='go-to-product js_conv js_clickHash js_seoUrl')
                    if
                    "promotion" not in product['href']]
        if len(products) < 1:
            logger.error("No products found at " + url)
            if kwargs.get("retry") > 0:
                logger.info('Retrying..')
                retries = kwargs.get("retry") - 1
                logger.info(str(retries) + " attempts left")
                return self.get_products(url, retry=retries)
            else:
                return None
        return products

    def __init__(self, product_name, offers_number=5, min_rating=4.0, min_reviews=20, min_price=0, max_price=999999):
        """
        CeneoScraper object containing offers for given product name that meets requirements(min rating and reviews count)

        :param str product_name:        Product name
        :param int offers_number:       Number of maximum product offers that meet requirements
        :param float min_rating:        Number of minimum product rating
        :param int min_reviews:         Number of minimum reviews count
        """
        self.OFFERS_NUMBER = offers_number
        self.MIN_RATING = min_rating
        self.MIN_REVIEWS = min_reviews
        self.productName = product_name
        self.products = self.get_products(CeneoScraper.create_url(product_name, min_price, max_price),
                                          retry=self.RETRY_NUMBER)
        if self.products:
            logger.info("Scraper for [" + self.productName + " ] initialized")
            self._allOffers = self._get_all_offers()
        else:
            self.productName = ""
            self._allOffers = {}
            logger.info("Scraper not initialized")

    def _get_all_offers(self):
        """
        It collects all offers for a given product,  maximum is equal to variable OFFERS_NUMBER

        :return:        List of dictionaries containing offer. It cointains product name, seller name, price,
                        delivery price, reviews number, reputation and url to a given item.
        """
        logger.info("Getting all offers..")
        all_offers_table, all_offers_description_table = self._get_tables()
        all_offers = []
        for index in range(len(all_offers_table)):
            price, delivery_price = TableScraper.get_price_from_table_element(all_offers_table[index])
            product_name = TableScraper.get_product_name_from_table_element(all_offers_table[index])
            shop_name = TableScraper.get_seller_name_from_table_description(all_offers_description_table[index])
            reviews_number = TableScraper.get_reviews_number_from_table_element(all_offers_table[index])
            rep = TableScraper.get_reputation_from_table_element(all_offers_table[index])
            url = TableScraper.get_offer_url_from_table_element(all_offers_table[index])
            all_offers.append(
                {"product_name": product_name, "seller_name": shop_name, "price": price,
                 "delivery_price": delivery_price,
                 "reviews_number": reviews_number, "rep": rep, "url": url})
            if len(all_offers) >= self.OFFERS_NUMBER:
                break
        logger.info(str(len(all_offers)) + " offers collected that meets requirements")
        return all_offers

    def _get_offers_from_product(self, product, **kwargs):
        """
        This function is loading given offer site (from product list). When its failed to load site it retries to a given
        RETRY_NUMBER times.

        :param list product:         List containing offers url from product search
        :param kwargs:               RETRY_NUMBER
        :return:                     Given offer page (soup)
        """
        try:
            product_page = BeautifulSoup(requests.get("https://www.ceneo.pl" + product['href'] + ";0284-0").text,
                                         'html.parser')
            if not product_page.find(class_="product-name"):
                raise WrongPageException()
        except WrongPageException:
            logger.error("No offers found at " + "https://www.ceneo.pl" + product['href'])
            if kwargs.get("retry") > 0:
                logger.info("Retrying..")
                retries = kwargs.get("retry") - 1
                logger.info(str(retries) + " attempts left")
                return self._get_offers_from_product(product, retry=retries)
            else:
                return None
        return product_page

    def _get_tables(self):
        """
        This function return table containg offers. This table will be scraped for a price, seller name etc.
        :return:        lists of table elements
        """
        all_offers_table = []
        all_offers_description_table = []
        for product in self.products:
            product_page = self._get_offers_from_product(product, retry=self.RETRY_NUMBER)
            if product_page:
                product_offers_table, product_offers_description_table = TableScraper.get_offers_table(product_page,
                                                                                                       self.MIN_RATING,
                                                                                                       self.MIN_REVIEWS)
                all_offers_table.extend(product_offers_table)
                all_offers_description_table.extend(product_offers_description_table)
            if len(all_offers_table) >= self.OFFERS_NUMBER:
                logger.info("Max offers number reached")
                break
        if len(all_offers_table) != len(all_offers_description_table):
            raise Exception(len(all_offers_description_table), "!=", len(all_offers_table))
        return all_offers_table, all_offers_description_table

    def get_product_name(self):
        return self.productName

    def get_all_offers(self):
        return self._allOffers

    def get_product_price(self):
        return [{key: item[key] for key in ['seller_name', 'price']} for item in self._allOffers]

    def get_product_rep(self):
        return [{key: item[key] for key in ['seller_name', 'rep', 'reviews_number']} for item in self._allOffers]

    def get_delivery_price(self):
        return [{key: item[key] for key in ['seller_name', 'delivery_price']} for item in self._allOffers]


page = CeneoScraper("jaguar xf", offers_number=5, min_rating=0, min_reviews=0, min_price=10000)

page2 = CeneoScraper("nokia 7.2", offers_number=5, min_rating=4.0, min_reviews=20, min_price=1000, max_price=10000)

page3 = CeneoScraper("iphone 10", offers_number=5, min_rating=4.0, min_reviews=20, min_price=2000)
