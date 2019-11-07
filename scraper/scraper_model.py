import requests
import logging
from bs4 import BeautifulSoup
from table_offer_scraper import TableScraper


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
        self.allOffers = self.get_all_offers()

    def get_all_offers(self):
        recommended_offers = TableScraper.get_reccomended_offers_table(self.productPage)
        other_offers = TableScraper.get_other_offers_table(self.productPage)
        all_offers_description = TableScraper.get_offers_description_table(self.productPage)
        all_offers = recommended_offers + other_offers

        for index in range(len(all_offers)):
            price = TableScraper.get_price_from_table_element(all_offers[index])
            shop_name = TableScraper.get_seller_name_from_table_element(all_offers_description[index])
            print(price, shop_name)

        return all_offers

    def get_product_price(self):
        return self.productPrice

    def get_product_name(self):
        return self.productName

    def get_product_rep(self):
        return self.productRep

    def get_delivery_price(self):
        return self.deliveryPrice


page = WebScraper("iphone 10")
print(page.get_product_name())
