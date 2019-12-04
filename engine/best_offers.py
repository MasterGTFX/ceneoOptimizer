from scraper import CeneoScraper

item1 = CeneoScraper("iphone xs", offers_number=5, min_rating=0, min_reviews=0, min_price=3000)
item2 = CeneoScraper("młotek", offers_number=5, min_rating=0, min_reviews=0, min_price=10)
item3 = CeneoScraper("powerbank", offers_number=5, min_rating=0, min_reviews=0, min_price=100)
item4 = CeneoScraper("zegarek", offers_number=5, min_rating=0, min_reviews=0, min_price=1000)
item5 = CeneoScraper("piekarnik", offers_number=5, min_rating=0, min_reviews=0, min_price=500)
prod1 = item1.get_all_offers()
prod2 = item2.get_all_offers()
prod3 = item3.get_all_offers()
prod4 = item4.get_all_offers()
prod5 = item5.get_all_offers()

#sorted_prod1=sorted(prod1, key = lambda i: (i['price']+i['delivery_price']))
print(prod1)
print(prod2)
print(prod3)
print(prod4)
print(prod5)

lista=[prod1, prod2, prod3, prod4, prod5]

def get_best_offers(lista):

    best_offers1 = []
    best_offers2 = []
    best_offers3 = []

    suma1 = 0.0
    suma2 = 0.0
    suma3 = 0.0

    zestawy = [best_offers1, best_offers2, best_offers3]

    for item in lista:
        item = sorted(item, key = lambda i: (i['price']+i['delivery_price']))

    for item in lista:
        best_offers1.append(item[0])
        best_offers2.append(item[1])
        best_offers3.append(item[2])

    for oferta in best_offers1:
        suma1 = suma1 + oferta['price'] + oferta['delivery_price']

    for oferta in best_offers2:
        suma2 = suma2 + oferta['price'] + oferta['delivery_price']

    for oferta in best_offers3:
        suma3 = suma3 + oferta['price'] + oferta['delivery_price']


    print("zestaw 1: koszt: ", suma1, best_offers1)
    print("zestaw 2: koszt: ", suma2, best_offers2)
    print("zestaw 3: koszt: ", suma3, best_offers3)



get_best_offers(lista)
