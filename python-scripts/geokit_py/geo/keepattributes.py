"""geo.addattributefc: Skeleton of a function."""

import json

from geojson.feature import FeatureCollection as fc
from smart_open import open


def keep_attributes(geojson_input: str, keys: list, geojson_out: str):
    """Script for keep props in each feature"""

    with open(geojson_input, encoding="utf8") as gfile:
        features_ = json.load(gfile).get("features", [])

    for feature in features_:
        properties = feature["properties"]

        for fprop in list(properties.keys()):
            if fprop not in keys:
                del properties[fprop]
        feature["properties"] = properties

        for fprop in list(feature.keys()):
            if fprop not in [*keys, "type", "properties", "geometry"]:
                del feature[fprop]

    print("================")
    print(f"Total  : {len(features_)} features")

    with open(geojson_out, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features_), ensure_ascii=False).encode("utf8").decode()
        )
