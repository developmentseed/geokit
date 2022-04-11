"""geo.renamekey: Skeleton of a function."""

import json

from geojson.feature import FeatureCollection as fc


def rename_key(geojson_input, props, geojson_output):
    """Script to rename one or more keys of the features"""
    with open(geojson_input, encoding="utf8") as gfile:
        features_ = json.load(gfile).get("features", [])
        for prop in props:
            if "=" not in prop:
                raise Exception(f"The property '{prop}' does not have the = symbol")
            if not len(prop.split("=")) == 2:
                raise Exception(
                    f"The property '{prop}' does not have the form old_key=new_key"
                )
            else:
                old_key, new_key = prop.strip().split("=")
                for i in features_:
                    properties = i.get("properties", "")
                    old_key_ = properties.get(old_key, "")
                    if old_key_:
                        properties[new_key] = properties[old_key]
                        del properties[old_key]

    with open(geojson_output, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features_), ensure_ascii=False).encode("utf8").decode()
        )
