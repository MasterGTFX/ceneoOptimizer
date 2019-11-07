from bs4 import BeautifulSoup
import logging
from regex_patterns import RegexPatterns


class TableScraper:
    @staticmethod
    def get_price_from_table_element(product):
        price_string = product.find('span', attrs={'class': "price"}).find(class_="value").text + product.find(
            'span',
            attrs={
                'class': "price"}).find(
            class_="penny").text.replace(",", ".")
        price = float(price_string)
        return price

    @staticmethod
    def get_seller_name_from_table_element(product_description):
        seller_name = product_description.find('a', attrs={'class': "js_product-offer-link"}).text
        return RegexPatterns.seller_name_regex.search(seller_name).group(1)

    @staticmethod
    def get_reccomended_offers_table(productPage):
        recommended_table = productPage.find('table', attrs={'class': 'product-offers js_product-offers'})
        recommended_products = recommended_table.find('tbody').find_all('tr', attrs={
            'class': 'product-offer'})
        return recommended_products

    @staticmethod
    def get_other_offers_table(productPage):
        others_table = productPage.find('table',
                                        attrs={'class': 'product-offers js_product-offers js_normal-offers'})
        others_products = others_table.find('tbody').find_all('tr', attrs={'class': 'product-offer'})
        return others_products

    @staticmethod
    def get_offers_description_table(productPage):
        all_products_description = productPage.find_all("tr", attrs={'class': 'details-row js_product-offer'})
        return all_products_description
