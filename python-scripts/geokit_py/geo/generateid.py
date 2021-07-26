"""geo.generateid: Skeleton of a function."""

import json
from uuid import uuid1
from smart_open import open
from geojson.feature import FeatureCollection as fc


def generateid(in_file, id_label, id_start, zeros, variation, output_file):
    """
    Add an id in the <properties> in a geojson file.
    """
    with open(in_file, "r", encoding="utf8") as gfile:
        json_data = json.load(gfile).get("features", [])

    for i, geo in enumerate(json_data, start=id_start):
        feature_props = geo["properties"]
        if variation.upper() == "uuid":
            feature_props[id_label] = uuid1().__str__()
        else:
            if zeros == 0:
                feature_props[id_label] = i
            else:
                feature_props[id_label] = str(i).zfill(zeros)

    with open(output_file, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(json_data), ensure_ascii=False).encode("utf8").decode()
        )
