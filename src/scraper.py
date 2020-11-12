import requests
from bs4 import BeautifulSoup
from operator import attrgetter
import json
import os


def get_geocode(adress: str):
    res = requests.post(
        "https://maps.googleapis.com/maps/api/geocode/json",
        params={"address": adress, "key": os.getenv("MAPS_API")},
    )

    return res.json()["results"][0]["geometry"]["location"]


def scrape_listing_urls(url: str, location: str, km: int):
    geocode = get_geocode(location)

    params = {
        "type": "for-rent",
        "filter_location": location,
        "lat": geocode["lat"],
        "lng": geocode["lng"],
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

    soup = BeautifulSoup(r.text, "html.parser")

    # extract json data
    scripts = soup.find_all("script", type="application/ld+json")
    json_raw_scripts = map(attrgetter("string"), scripts)
    # parse to json
    json_parsed_scripts = list(map(json.loads, json_raw_scripts))

    # consider only data we want
    data = list(
        filter(
            lambda x: type(x.get("@type")) is list and "House" in x.get("@type"),
            json_parsed_scripts,
        )
    )[0]

    offers = data.get("offers", {})

    try:
        price = float(offers.get("price", None))
    except ValueError:
        price = None

    base_data = {
        "name": data.get("name", None),
        "description": data.get("description", None),
        "price": price,
        "currency": offers.get("priceCurrency", None),
        "url": data.get("url", None),
    }

    # extract image urls
    images = soup.find("div", {"class": "single_media"}).find_all("a")
    json_raw_img_urls = map(lambda x: x.get("href", None), images)
    img_data = list(json_raw_img_urls)

    final_data = {
        "base_data": base_data,
        "img_data": img_data,
    }

    return final_data


#####################################################################################
#                                   Client code                                     #
#####################################################################################


urls1 = scrape_listing_urls("https://househunting.nl/woningaanbod/", "Eindhoven", 5)
#  urls2 = scrape_listing_urls("https://househunting.nl/woningaanbod/", "Amsterdam", 5)
#  urls = urls1 + urls2

data = list(map(lambda url: scrape_listing(url), urls1))

for d in data:
    res = requests.post(
        os.getenv("SCRAPER_BACKEND_URL"),
        json=d,
        headers={"Content-Type": "application/json"},
    )
    print(res.json())
