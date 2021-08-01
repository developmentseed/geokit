"""rl_schoolspoint.process: Skeleton of a function."""

import logging

import requests
from bs4 import BeautifulSoup


def process(city):
    """
    Get points of schools from https://www.international-schools-database.com.
    """
    URL = f"https://www.international-schools-database.com/in/{city}"
    try:
        page = requests.get(URL)
        features = []
        soup = BeautifulSoup(page.content, "html.parser")
        fullscreen_map = soup.find(id="fullscreen-map")
        if fullscreen_map:
            for i in fullscreen_map.find_all("span"):
                if i and i.get("data-marker-longitude"):
                    feature = {
                        "type": "Feature",
                        "properties": {
                            "name": i.get("data-marker-name"),
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                float(i.get("data-marker-longitude")),
                                float(i.get("data-marker-latitude")),
                            ],
                        },
                    }
                    features.append(feature)
        else:
            logging.error("No se encontraron resultados.")
            return ""
    except Exception as e:
        logging.error(e.__str__())
    else:
        data = {"type": "FeatureCollection", "features": features}
        print(data)
