from scraper import CeneoScraper

item1 = CeneoScraper("iphone xs", offers_number=5, min_rating=0, min_reviews=0, min_price=3000)
item2 = CeneoScraper("młotek", offers_number=5, min_rating=0, min_reviews=0, min_price=10)
item3 = CeneoScraper("powerbank", offers_number=5, min_rating=0, min_reviews=0, min_price=100)
item4 = CeneoScraper("nokia", offers_number=5, min_rating=0, min_reviews=0, min_price=1000)
item5 = CeneoScraper("piekarnik", offers_number=5, min_rating=0, min_reviews=0, min_price=500)
prod1 = item1.get_all_offers()
prod2 = item2.get_all_offers()
prod3 = item3.get_all_offers()
prod4 = item4.get_all_offers()
prod5 = item5.get_all_offers()

lista=[prod1, prod2, prod3, prod4, prod5]

def get_best_offers(offers_list):

    first_set = []
    second_set = []
    third_set = []

    first_set_price = 0.0
    second_set_price = 0.0
    third_set_price = 0.0

    for item in offers_list:
        item = sorted(item, key = lambda i: (i['price']+i['delivery_price']))

    for item in offers_list:
        first_set.append(item[0])
        second_set.append(item[1])
        third_set.append(item[2])

    sets = [first_set, second_set, third_set]

    for set in sets:
        for i in range(0, len(set)):
            inc = 0
            discount = 0.0
            for j in range(1, len(set) - 2):
                if set[i]['seller_name'] == set[j]['seller_name']:
                    inc+=1
            if inc:
                set[i]['price'] = set[i]['price'] - inc * set[i]['delivery_price']



    for offer in first_set:
        first_set_price = first_set_price + offer['price'] + offer['delivery_price']

    for offer in second_set:
        second_set_price = second_set_price + offer['price'] + offer['delivery_price']

    for offer in third_set:
        third_set_price = third_set_price + offer['price'] + offer['delivery_price']

    best_offers = [first_set, first_set_price, second_set, second_set_price, third_set, third_set_price]
    return best_offers

print(get_best_offers(lista))
