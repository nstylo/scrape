import requests
from bs4 import BeautifulSoup
from operator import attrgetter
import json
import os


def scrape_listing_urls(url: str, location: str, km: int):
    params = {
        "type": "for-rent",
        "filter_location": location,
        "lat": "51.441641",  # TODO: connect to geolocation api
        "lng": "5.4697225",
        "street": "",
        "km": km,
        "min-price": "",
        "max-price": "",
    }

    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "html.parser")

    urls = soup.find_all("a", title=True)

    return list(map(lambda x: x.get("href"), urls))


def scrape_listing(url: str):
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

    try:
        price = float(offers.get("price", None))
    except ValueError:
        price = None

    return {
        "name": data.get("name", None),
        "description": data.get("description", None),
        "price": price,
        "currency": offers.get("priceCurrency", None),
        "url": data.get("url", None),
    }


urls = scrape_listing_urls("https://househunting.nl/woningaanbod/", "Eindhoven", 5)
data = list(map(lambda url: parse_listing(scrape_listing(url)), urls))

for d in data:
    res = requests.post(
        os.getenv("SCRAPER_BACKEND_URL"),
        json=d,
        headers={"Content-Type": "application/json"},
    )
    print(res.json())