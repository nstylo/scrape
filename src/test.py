import requests
from bs4 import BeautifulSoup
from operator import attrgetter
import json

r = requests.get(
    "https://househunting.nl/woningaanbod/h103400217-landbouwstraat-tilburg/",
    #  data={"email": "n.michael.sdu@gmail.com", "password": "1022355Aa!"},
)

soup = BeautifulSoup(r.text, "html.parser")

scripts = soup.find_all("script", type="application/ld+json")

json_raw = map(attrgetter("string"), scripts)

json_parsed = map(json.loads, json_raw)

print(list(json_parsed))


class Data:
    """"""

    def __init__(self, payload):
        self.payload = payload
        #  self.name = None
        #  self.description = None
        #  self.price = None
        #  self.url = None
        #  self.address = None

    @property
    def name(self):
        pass

    @property
    def description(self):
        pass

    @property
    def price(self):
        pass

    @property
    def url(self):
        pass

    @property
    def address(self):
        pass
