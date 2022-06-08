"""geo.deletenulls: Skeleton of a function."""

import json
from geojson.feature import FeatureCollection as fc


def delete_null_values(geojson_input, geojson_output, delete_feat):
    """Script to delete the attributes that have a null value."""

    with open(geojson_input, encoding="utf8") as gfile:
        features_ = json.load(gfile).get("features", [])

        crit_evaluar = [None, {}, [], ""]
        for element in features_:
            properties = element["properties"]
            items = list(properties.items())

            for k, v in items:
                if v in crit_evaluar:
                    if delete_feat:
                        element["delete"] = True
                    else:
                        del properties[k]

        clean_feat = [i for i in features_ if not i.get("delete")]

    with open(geojson_output, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(clean_feat), ensure_ascii=False).encode("utf8").decode()
        )
