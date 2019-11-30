import requests
from bs4 import BeautifulSoup as bs
import sys
import json


#slownik = {"klucz1":41, "klucz2":2, "klucz3":20}
slownik2 = {"sys.argv[0]": sys.argv[0],"sys.argv[1]": sys.argv[1],"sys.argv[2]": sys.argv[2],"sys.argv[3]": sys.argv[3], "len": len(sys.argv)}
y = json.dumps(slownik2)

print(y)
sys.stdout.flush()
