import requests
import logging
from bs4 import BeautifulSoup
from table_offer_scraper import TableScraper
import sys
import json

class WebScraper:

    @staticmethod
    def create_url(productName):
        return "https://www.ceneo.pl/szukaj-" + productName

    @staticmethod
    def get_page(url):
        allProductsPage = BeautifulSoup(requests.get(url).text, 'html.parser')
        products = [product for product in
                    allProductsPage.find_all(class_='go-to-product js_conv js_clickHash js_seoUrl')
                    if
                    "promotion" not in product['href']]
        return BeautifulSoup(requests.get("https://www.ceneo.pl" + products[0]['href']).text,
                             'html.parser')

    def __init__(self, productName):
        self.productPage = WebScraper.get_page(WebScraper.create_url(productName))
        self.productName = self.productPage.find(
            class_="product-name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").text
        self._allOffers = self.get_all_offers()

    def get_all_offers(self):
        recommended_offers_table = TableScraper.get_reccomended_offers_table(self.productPage)
        other_offers_table = TableScraper.get_other_offers_table(self.productPage)
        all_offers_description_table = TableScraper.get_offers_description_table(self.productPage)
        all_offers_table = recommended_offers_table + other_offers_table
        all_offers = []
        if len(all_offers_table) != len(all_offers_description_table):
            raise Exception(len(all_offers_description_table), "!=", len(all_offers_table))
        for index in range(len(all_offers_table)):
            price = TableScraper.get_price_from_table_element(all_offers_table[index])
            shop_name = TableScraper.get_seller_name_from_table_description(all_offers_description_table[index])
            reviews_number = TableScraper.get_reviews_number_from_table_element(all_offers_table[index])
            rep = TableScraper.get_reputation_from_table_element(all_offers_table[index])
            all_offers.append({"seller_name": shop_name, "price": price, "reviews_number": reviews_number, "rep": rep})
        return all_offers

    def get_product_price(self):
        return self.productPrice

    def get_product_name(self):
        return self.productName

    def get_product_rep(self):
        return self.productRep

    def get_delivery_price(self):
        return self.deliveryPrice


page = WebScraper("nokia 7.2")
print(page.get_product_name())
y = json.dumps(page.get_all_offers())

print(y)
sys.stdout.flush()



