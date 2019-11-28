import requests
from bs4 import BeautifulSoup
from offer_scraper import TableScraper


class WrongPageException(BaseException):
    pass


class CeneoScraper:
    RETRY_NUMBER = 5

    @staticmethod
    def create_url(productName):
        return "https://www.ceneo.pl/szukaj-" + productName

    def get_page(self, url, **kwargs):
        all_products_page = BeautifulSoup(requests.get(url).text, 'html.parser')
        products = [product for product in
                    all_products_page.find_all(class_='go-to-product js_conv js_clickHash js_seoUrl')
                    if
                    "promotion" not in product['href']]
        try:
            product_page = BeautifulSoup(requests.get("https://www.ceneo.pl" + products[0]['href'] + ";0284-0").text,
                                         'html.parser')
            if product_page.find(class_="product-name"):
                print("[INFO] Product page looking good")
            else:
                raise WrongPageException()
            return product_page, products
        except (IndexError, AttributeError, WrongPageException):
            print("[ERROR] No products found at " + url)
            if kwargs.get("retry") > 0:
                print("[INFO] Retrying..")
                retries = kwargs.get("retry") - 1
                print("[INFO] " + str(retries) + " attempts left")
                return self.get_page(url, retry=retries)
            else:
                return None, None

    def __init__(self, productName, **kwargs):
        self.OFFERS_NUMBER = kwargs.get('OFFERS_NUMBER') if kwargs.get('OFFERS_NUMBER') else 5
        self.MIN_RATING = kwargs.get('MIN_RATING') if kwargs.get('MIN_RATING') else 4.0
        self.REVIEWS_NUMBER = kwargs.get('REVIEWS_NUMBER') if kwargs.get('REVIEWS_NUMBER') else 20
        self.productName = productName
        self.productPage, self.products = self.get_page(CeneoScraper.create_url(productName), retry=self.RETRY_NUMBER)
        if self.productPage:
            self._allOffers = self._get_all_offers()
            print("[INFO] Scraper for [" + self.productName + " ] initialized")
        else:
            self.productName = ""
            self._allOffers = {}
            print("[INFO] Scraper not initialized")

    def _get_all_offers(self):
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
                print("[INFO] Max offers number reached")
                break
        print("[INFO] Total: " + str(len(all_offers)) + " offers saved")
        return all_offers

    def _get_tables(self):
        all_offers_table = TableScraper.get_offers_table(self.productPage)
        all_offers_description_table = TableScraper.get_offers_description_table(self.productPage)
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


page = CeneoScraper("jaguar xf", OFFERS_NUMBER=5, MIN_RATING=4.0, REVIEWS_NUMBER=20)

page2 = CeneoScraper("nokia 7.2", OFFERS_NUMBER=5, MIN_RATING=4.0, REVIEWS_NUMBER=20)

page3 = CeneoScraper("iphone 10", OFFERS_NUMBER=5, MIN_RATING=4.0, REVIEWS_NUMBER=20)
