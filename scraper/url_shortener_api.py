import requests
import json
import logging


class UrlShortener:
    API_KEY = "R_cc1f7a8bfd1e4ce2903db98c2606d716"

    def __init__(self):
        self.baseurl = "https://api-ssl.bitly.com/v3/shorten"

    def shorten(self, url):
        parameters = {
            'access_token': self.API_KEY,
            'longUrl': url
        }
        response = requests.get(self.baseurl, params=parameters, verify=False)
        data = response.json()

        if not data['status_code'] == 200:
            raise ConnectionError("Unexpected status_code: {} in bitly response. {}".format(data['status_code'], response.text))

        return data['data']['url']


a = UrlShortener()
print(a.shorten("google.com"))
