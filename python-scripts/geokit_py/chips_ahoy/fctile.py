"""
Script for add tile and url in features.

Author: @developmentseed
"""
import json
import logging
from uuid import uuid1
from itertools import islice

import mercantile
from geojson import FeatureCollection as fc
from shapely.geometry import shape
from smart_open import open
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def chunk(it, size):
    """Return list of chuks by size."""
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def get_tile(feature, zoom, url_map_service):
    """Return feature with tile and url properties."""
    geom = shape(feature["geometry"])
    centroid = geom.centroid
    tile = mercantile.tile(centroid.x, centroid.y, zoom)
    props = feature["properties"]
    props["uuid"] = uuid1().__str__()
    props["tile"] = f"{tile.x}-{tile.y}-{tile.z}"
    props["url"] = url_map_service.format(x=tile.x, z=tile.z, y=tile.y)
    return feature


def fctile(geojson_file, zoom, url_map_service, geojson_output, chuck):
    """Script for add tile and url in features."""
    with open(geojson_file, encoding="utf8") as gfile:
        features = json.load(gfile).get("features", [])

    new_features = [
        get_tile(feature, zoom, url_map_service)
        for feature in tqdm(features, desc=f"get tile at zoom={zoom}")
    ]

    logging.info(f"Total features : {len(new_features)}")

    if chuck:
        for k, i in enumerate(list(chunk(new_features, chuck))):
            with open(
                    geojson_output.replace(".geojson", f"_{k}.geojson"), "w"
            ) as out_geo:
                out_geo.write(
                    json.dumps(fc(i), ensure_ascii=False).encode("utf8").decode()
                )
    else:
        with open(geojson_output, "w") as out_geo:
            out_geo.write(
                json.dumps(fc(new_features), ensure_ascii=False).encode("utf8").decode()
            )
