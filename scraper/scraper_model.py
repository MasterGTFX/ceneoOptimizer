import requests
from bs4 import BeautifulSoup
from offer_scraper import TableScraper


class WrongPageException(BaseException):
    pass


class CeneoScraper:
    RETRY_NUMBER = 5

    @staticmethod
    def create_url(productName):
        """
        :param productName:         Product to be searched
        :return:                    Url for ceneo search to a given product
        """
        return "https://www.ceneo.pl/szukaj-" + productName

    def get_products(self, url, **kwargs):
        """

        :param url:     Link to search result page for given product name
        :return:        List containing products href
        """
        all_products_page = BeautifulSoup(requests.get(url).text, 'html.parser')
        products = [product for product in
                    all_products_page.find_all(class_='go-to-product js_conv js_clickHash js_seoUrl')
                    if
                    "promotion" not in product['href']]
        if len(products) < 1:
            print("[ERROR] No products found at " + url)
            if kwargs.get("retry") > 0:
                print("[INFO] Retrying..")
                retries = kwargs.get("retry") - 1
                print("[INFO] " + str(retries) + " attempts left")
                return self.get_products(url, retry=retries)
            else:
                return None
        return products

    def __init__(self, product_name, OFFERS_NUMBER=5, MIN_RATING=4.0, MIN_REVIEWS=20):
        """
        CeneoScraper object containing offers for given product name that meets requirements(min rating and reviews count)

        :param product_name:        Product name
        :param OFFERS_NUMBER:       Number of maximum product offers that meet requirements
        :param MIN_RATING:          Number of minimum product rating
        :param MIN_REVIEWS:         Number of minimum reviews count
        """
        self.OFFERS_NUMBER = OFFERS_NUMBER
        self.MIN_RATING = MIN_RATING
        self.MIN_REVIEWS = MIN_REVIEWS
        self.productName = product_name
        self.products = self.get_products(CeneoScraper.create_url(product_name), retry=self.RETRY_NUMBER)
        if self.products:
            print("[INFO] Scraper for [" + self.productName + " ] initialized")
            self._allOffers = self._get_all_offers()
        else:
            self.productName = ""
            self._allOffers = {}
            print("[INFO] Scraper not initialized")

    def _get_all_offers(self):
        """
        It collects all offers for a given product,  maximum is equal to variable OFFERS_NUMBER

        :return:        List of dictionaries containing offer. It cointains product name, seller name, price,
                        delivery price, reviews number, reputation and url to a given item.
        """
        print("[INFO] Getting all offers..")
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
        print("[INFO] " + str(len(all_offers)) + " offers collected that meets requirements")
        return all_offers

    def _get_offers_from_product(self, product, **kwargs):
        """
        This function is loading given offer site (from product list). When its failed to load site it retries to a given
        RETRY_NUMBER times.

        :param product:         List containing offers url from product search
        :param kwargs:          RETRY_NUMBER
        :return:                Given offer page (soup)
        """
        try:
            product_page = BeautifulSoup(requests.get("https://www.ceneo.pl" + product['href'] + ";0284-0").text,
                                         'html.parser')
            if not product_page.find(class_="product-name"):
                raise WrongPageException()
        except WrongPageException:
            print("[ERROR] No offers found at " + "https://www.ceneo.pl" + product['href'])
            if kwargs.get("retry") > 0:
                print("[INFO] Retrying..")
                retries = kwargs.get("retry") - 1
                print("[INFO] " + str(retries) + " attempts left")
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
                print("[INFO] Max offers number reached")
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


page = CeneoScraper("jaguar xf", OFFERS_NUMBER=5, MIN_RATING=0, MIN_REVIEWS=0)

page2 = CeneoScraper("nokia 7.2", OFFERS_NUMBER=5, MIN_RATING=4.0, MIN_REVIEWS=20)

page3 = CeneoScraper("iphone 10", OFFERS_NUMBER=5, MIN_RATING=4.0, MIN_REVIEWS=20)
