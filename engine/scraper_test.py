import requests
from bs4 import BeautifulSoup as bs
import sys
import json

#item_params_len = int(sys.argv[2])
#items_len = int(sys.argv[3])

#list = []


#data = json.loads(sys.argv[1])

data = {'Item_0': {'Product name': 'chuj', 'Max price': '100', 'Min price': '2', 'Min rating': '1', 'Min reviews': '3', 'Num offers': '2', 'Num products': '2'}, 'Item_1': {'Product name': 'dsa', 'Max price': '200', 'Min price': '123', 'Min rating': '212', 'Min reviews': '21', 'Num offers': '2', 'Num products': '2'}}


#print(data[0])
#print("json python")
#print(data)
#print("ok")

#print(data['Item_1'])


products_params = []
lista_ofert = []


for i in data:
    for j in data[i]:
        print(j + "--"+ data[i][j])
        if(j=="Product name"):
            products_params.append(data[i][j])
        elif(j=="Max price"):
            products_params.append(float(data[i][j]))
        elif(j=="Min price"):
            products_params.append(float(data[i][j]))
        elif(j=="Min rating"):
            products_params.append(float(data[i][j]))
        elif(j=="Min reviews"):
            products_params.append(float(data[i][j]))
        elif(j=="Num offers"):
            products_params.append(float(data[i][j]))
        elif(j=="Num offers"):
            products_params.append(float(data[i][j]))
    oferty = products_params[0], products_params[0], products_params[3], products_params[4], products_params[2]
    #oferty = CeneoScraper(products_params[0], products_params[5], products_params[3], products_params[4], products_params[2]).get_all_offers()
    lista_ofert.append(oferty)
    products_params = []


#CeneoScraper(item_name, offers_number, min_rating, min_reviews, min_price)

#for j in range(items_len):
#    item_name = sys.argv[1][7*j]
#    offers_number = float(sys.argv[1][5+7*j])
#    min_rating = float(sys.argv[1][3+7*j])
#    min_reviews = float(sys.argv[1][4+7*j])
#    min_price = float(sys.argv[1][2+7*j])
#print(data)
#print(data[0])



#slownik = {"klucz1":41, "klucz2":2, "klucz3":20}
#slownik2 = {"paramy": sys.argv[1].len, "len": len(sys.argv)}
#y = json.dumps(slownik2)

sys.stdout.flush()
