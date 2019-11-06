import requests
import logging
from bs4 import BeautifulSoup
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
        self.allOffers = self.get_all_offers()

    def get_all_offers(self):
        recommended_table = self.productPage.find('table', attrs={'class': 'product-offers js_product-offers'})
        recommended_products = recommended_table.find('tbody').find_all('tr', attrs={
            'class': 'product-offer'})
        others_table = self.productPage.find('table',
                                             attrs={'class': 'product-offers js_product-offers js_normal-offers'})
        others_products = others_table.find('tbody').find_all('tr', attrs={'class': 'product-offer'})
        all_products = recommended_products + others_products
        for product in all_products:
            price = self.get_price_of_table_element(product)
            print(price)
        return all_products

    def get_price_of_table_element(self, product):
        if product.has_attr('data-price'):
            price = product['data-price']
        else:
            price_string = product.find('span', attrs={'class': "price"}).find(class_="value").text + product.find(
                'span',
                attrs={
                    'class': "price"}).find(
                class_="penny").text.replace(",", ".")
            price = float(price_string)
        return price

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
