"""geo.deletenulls: Skeleton of a function."""

import json
from copy import deepcopy

from geojson.feature import FeatureCollection as fc


def delete_null_values(geojson_input, geojson_output, delete_feat):
    """Script to delete the attributes that have a null value."""
    with open(geojson_input, encoding="utf8") as gfile:
        features_ = json.load(gfile).get("features", [])
        features_temp = deepcopy(features_)

        crit_evaluar = [None, {}, [], ""]
        for i, element in enumerate(features_):
            properties = element["properties"]
            for k, v in list(properties.items()):
                if v in crit_evaluar:
                    if delete_feat:
                        features_[i] = None
                    else:
                        del features_temp[i]["properties"][k]

        clean_feat = [i for i in features_ if i]

    if delete_feat:
        with open(geojson_output, "w") as out_geo:
            out_geo.write(
                json.dumps(fc(clean_feat), ensure_ascii=False).encode("utf8").decode()
            )
    else:
        with open(geojson_output, "w") as out_geo:
            out_geo.write(
                json.dumps(fc(features_temp), ensure_ascii=False)
                .encode("utf8")
                .decode()
            )
