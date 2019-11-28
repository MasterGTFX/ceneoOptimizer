import requests
from bs4 import BeautifulSoup
from offer_scraper import TableScraper


class WrongPageException(BaseException):
    pass


class CeneoScraper:
    OFFERS_NUMBER = 5
    MIN_RATING = 4
    MIN_REPUTATION = 20
    RETRY_NUMBER = 5

    @staticmethod
    def create_url(productName):
        return "https://www.ceneo.pl/szukaj-" + productName

    def get_page(self, url, **kwargs):
        allProductsPage = BeautifulSoup(requests.get(url).text, 'html.parser')
        products = [product for product in
                    allProductsPage.find_all(class_='go-to-product js_conv js_clickHash js_seoUrl')
                    if
                    "promotion" not in product['href']]
        try:
            productPage = BeautifulSoup(requests.get("https://www.ceneo.pl" + products[0]['href']).text,
                                        'html.parser')
            if productPage.find(class_="product-name"):
                print("[INFO] Product page looking good")
            else:
                raise WrongPageException()
            return productPage, products
        except (IndexError, AttributeError, WrongPageException):
            print("[ERROR] No products found at " + url)
            if kwargs.get("retry") > 0:
                print("[INFO] Retrying..")
                retries = kwargs.get("retry") - 1
                print("[INFO] " + str(retries) + " attempts left")
                return self.get_page(url, retry=retries)
            else:
                return None, None

    def __init__(self, productName):
        self.productPage, self.products = self.get_page(CeneoScraper.create_url(productName), retry=self.RETRY_NUMBER)
        if self.productPage:
            self.productName = self.productPage.find(class_="product-name").text
            self._allOffers = self._get_all_offers()
            print("[INFO] Scraper for " + self.productName + " initialized")
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
            shop_name = TableScraper.get_seller_name_from_table_description(all_offers_description_table[index])
            reviews_number = TableScraper.get_reviews_number_from_table_element(all_offers_table[index])
            rep = TableScraper.get_reputation_from_table_element(all_offers_table[index])
            url = TableScraper.get_offer_url_from_table_element(all_offers_table[index])
            all_offers.append(
                {"seller_name": shop_name, "price": price, "delivery_price": delivery_price,
                 "reviews_number": reviews_number, "rep": rep, "url": url})
            if len(all_offers) >= self.OFFERS_NUMBER:
                print("[INFO] Max offers number reached")
                break
        print("[INFO] Total: " + str(len(all_offers)) + " offers received")
        return all_offers

    def _get_tables(self):
        recommended_offers_table = TableScraper.get_reccomended_offers_table(self.productPage)
        other_offers_table = TableScraper.get_other_offers_table(self.productPage)
        all_offers_description_table = TableScraper.get_offers_description_table(self.productPage)
        all_offers_table = recommended_offers_table + other_offers_table
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


page = CeneoScraper("jaguar xf")
print(page.get_product_name())

page2 = CeneoScraper("nokia 7.2")
print(page2.get_product_name())

page3 = CeneoScraper("iphone 10")
print(page3.get_product_name())
