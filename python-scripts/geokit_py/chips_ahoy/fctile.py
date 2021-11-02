"""
Script for add tile and url in features.

Author: @developmentseed
"""
import json
import logging
from itertools import islice
from uuid import uuid1

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


def get_tile(feature, zoom, url_map_service, is_super_tile):
    """Return feature with tile and url properties."""
    geom = shape(feature["geometry"])
    centroid = geom.centroid
    tile = mercantile.tile(centroid.x, centroid.y, zoom)
    props = feature["properties"]
    props["uuid"] = uuid1().__str__()
    props["tile"] = f"{tile.x}-{tile.y}-{tile.z}"
    props["url"] = url_map_service.format(x=tile.x, z=tile.z, y=tile.y)
    if is_super_tile:
        tiles_neighbors = mercantile.neighbors(tile)
        tiles_neighbors_dict = {}
        for k, t_n in enumerate(tiles_neighbors):
            tiles_neighbors_dict[f"tn_{k}"] = url_map_service.format(
                x=t_n.x, z=t_n.z, y=t_n.y
            )

        props["tiles_neighbors"] = tiles_neighbors_dict
    return feature


def fctile(geojson_file, zoom, url_map_service, geojson_output, chuck, is_super_tile):
    """Script for add tile and url in features."""
    with open(geojson_file, encoding="utf8") as gfile:
        features = json.load(gfile).get("features", [])

    new_features = [
        get_tile(feature, zoom, url_map_service, is_super_tile)
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
