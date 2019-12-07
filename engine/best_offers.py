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
