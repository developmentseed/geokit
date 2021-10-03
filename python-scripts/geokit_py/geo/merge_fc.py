"""geo.merge_fc: Skeleton of a function."""
from geojson.feature import FeatureCollection as fc
from smart_open import open
import json


def merge_features(geojson_inputs, geojson_output):
    """Script to merge features."""
    features = []
    print("==================")
    for geojson in geojson_inputs:
        geojson_data = json.load(open(geojson)).get("features", [])
        features += geojson_data
        print(f"{geojson.split('/')[-1]}: \t{str(len(geojson_data)).zfill(4)}")
    print(f"total output: \t{str(len(features)).zfill(4)}")
    print("==================")
    with open(geojson_output, "w") as f:
        f.write(json.dumps(fc(features), ensure_ascii=False).encode("utf8").decode())
