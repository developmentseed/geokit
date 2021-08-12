"""geo.duplicate_features_by_tag: Skeleton of a function."""

import json

from geojson.feature import FeatureCollection as fc
from smart_open import open
from tqdm import tqdm
import collections


def duplicate_features_by_tag(geojson_input, key, geojson_output):
    """
    Difference between two geojson files according to an attribute
    """
    with open(geojson_input, "r", encoding="utf8") as gfile:
        json_data = json.load(gfile).get("features", [])

    ids = [
        feat["properties"].get(key) for feat in json_data if feat["properties"].get(key)
    ]
    id_duplicates = [
        item for item, count in collections.Counter(ids).items() if count > 1
    ]

    feat_duplicates = []

    for feature in tqdm(json_data, desc=f"Filter duplicates of {key} "):
        val = feature["properties"].get(key)
        if val in id_duplicates:
            feat_duplicates.append(feature)
    print(
        f"We found {str(len(id_duplicates)).zfill(3)} ids duplicates, {str(len(feat_duplicates)).zfill(3)} features duplicates"
    )
    with open(geojson_output, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(feat_duplicates), ensure_ascii=False).encode("utf8").decode()
        )
