from regex_patterns import RegexPatterns


class TableScraper:

    @staticmethod
    def get_offers_table(productPage):
        print("[INFO] Searching for offers")
        others_table = productPage.find('table',
                                        attrs={'class': 'product-offers js_product-offers js_normal-offers'})
        others_products = others_table.find('tbody').find_all('tr', attrs={'class': 'product-offer'})
        print("[INFO] " + str(len(others_products)) + " offers found")
        return others_products

    @staticmethod
    def get_offers_description_table(productPage):
        all_products_description = productPage.find_all("tr", attrs={'class': 'details-row js_product-offer'}) + \
                                   productPage.find_all("tr", attrs={
                                       'class': 'details-row js_appendRemainingAfter js_product-offer'})
        return all_products_description

    @staticmethod
    def get_price_from_table_element(product):
        price_string = product.find('span', attrs={'class': "price"}).find(class_="value").text + product.find(
            'span',
            attrs={
                'class': "price"}).find(
            class_="penny").text.replace(",", ".")
        price_table = product.find('td', attrs={'class': "cell-price"})
        if price_table.find("span", attrs={'class': "free-delivery-txt"}):
            delivery_price = 0.0
        else:
            delivery_price_text = price_table.find("div", attrs={'class': "product-delivery-info js_deliveryInfo"}).text
            if RegexPatterns.deliver_price_regex.search(delivery_price_text):
                total_price = RegexPatterns.deliver_price_regex.search(delivery_price_text).group().replace(",", ".")
                delivery_price = float(total_price) - float(price_string)
            else:
                delivery_price = 0.0
        return float(price_string), delivery_price

    @staticmethod
    def get_product_name_from_table_element(product):
        product_name = product.find('span', attrs={'class': 'short-name__txt'}).text
        return product_name

    @staticmethod
    def get_seller_name_from_table_description(product_description):
        seller_name = product_description.find('a', attrs={'class': "js_product-offer-link"}).text
        return RegexPatterns.seller_name_regex.search(seller_name).group(1)

    @staticmethod
    def get_reviews_number_from_table_element(product):
        number_of_reviews_string = product.find('span',
                                                attrs={'class': "dotted-link js_mini-shop-info js_no-conv"}).text
        return int(RegexPatterns.number_of_reviews_regex.search(number_of_reviews_string).group(1))

    @staticmethod
    def get_reputation_from_table_element(product):
        reputation_table = product.find('td', attrs={'class': "cell-store-review"})
        reputation = reputation_table.find('span', attrs={'class': 'screen-reader-text'}).text
        return float(RegexPatterns.reputation_regex.search(reputation).group(1).replace(",", "."))

    @staticmethod
    def get_offer_url_from_table_element(product):
        url_table = product.find('td', attrs={'class': "cell-price"})
        url = url_table.find('a', attrs={'class': 'product-price go-to-shop'})['href']
        return "https://www.ceneo.pl/" + str(url)
