"""geo.difference_by_tag: Skeleton of a function."""

import json

from geojson.feature import FeatureCollection as fc
from smart_open import open
from tqdm import tqdm


def difference_by_tag(geojson_input, geojson_dif, key, geojson_output):
    """
    Difference between two geojson files according to an attribute
    """
    with open(geojson_input, "r", encoding="utf8") as gfile:
        json_data = json.load(gfile).get("features", [])
    with open(geojson_dif, "r", encoding="utf8") as gfile:
        json_dif_data = json.load(gfile).get("features", [])

    feature_obj = []

    for di_fe in tqdm(json_dif_data, desc=f"Filter values of {key} "):
        val = di_fe["properties"].get(key)
        if val:
            feature_obj.append(val)
    # remove duplicates
    feature_obj = list(dict.fromkeys([i for i in feature_obj if i]))
    features_out = []

    for feature in tqdm(json_data, desc="Filter  geojson_input "):
        if not feature["properties"].get(key) in feature_obj:
            features_out.append(feature)

    with open(geojson_output, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features_out), ensure_ascii=False).encode("utf8").decode()
        )
