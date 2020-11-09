import requests
from bs4 import BeautifulSoup
from operator import attrgetter
import json


def scrape_listing(url):
    # make request
    r = requests.get(url)

    # extract json data
    soup = BeautifulSoup(r.text, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    json_raw = map(attrgetter("string"), scripts)

    # parse to json
    return list(map(json.loads, json_raw))


def parse_listing(data: list):
    # precondition
    if not type(data) is list:
        raise Exception(
            "parse_data: <class 'list'> expected, {} given.".format(type(data))
        )

    # consider only data we want
    data = list(
        filter(
            lambda x: type(x.get("@type")) is list and "House" in x.get("@type"), data
        )
    )[0]

    offers = data.get("offers", {})

    return {
        "name": data.get("name", None),
        "description": data.get("description", None),
        "price": offers.get("price", None),
        "currency": offers.get("priceCurrency", None),
        "url": data.get("url", None),
    }


urls = [
    "https://househunting.nl/woningaanbod/h103400217-landbouwstraat-tilburg/",
    "https://househunting.nl/woningaanbod/h103400311-vier-heultjes-sprang-capelle/",
    "https://househunting.nl/woningaanbod/h103321275-boutenslaan-eindhoven/",
    "https://househunting.nl/woningaanbod/h103420713-alexander-numankade-utrecht/",
]
for url in urls:
    data = scrape_listing(url)
    print(parse_listing(data))
