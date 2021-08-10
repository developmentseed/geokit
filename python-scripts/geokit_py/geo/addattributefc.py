"""geo.addattributefc: Skeleton of a function."""

import json

from geojson.feature import FeatureCollection as fc
from smart_open import open


def add_attribute_fc(
        geojson_in_features: str,
        props_feature: list,
        geojson_out_features: str
):
    """Script for add props in each feature"""

    with open(geojson_in_features, encoding="utf8") as gfile:
        features_ = json.load(gfile).get("features", [])

    for feature in features_:
        for prop in props_feature:
            prop_ = prop.strip().replace('"', '').split("=")
            feature["properties"][str(prop_[0])] = prop_[1]

    print("================")
    print(f"Total  : {len(features_)} features")
    print("====== STATS ==========")
    with open(geojson_out_features, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features_), ensure_ascii=False)
                .encode("utf8")
                .decode()
        )
