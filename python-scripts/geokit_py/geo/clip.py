import geopandas as gpd
from smart_open import open
import json


def clip(geojson_input, geojson_boundary, geojson_output):
    """Script to clip features"""
    features_inp = json.load(open(geojson_input)).get("features")
    data = gpd.GeoDataFrame.from_features(features_inp)

    features_bound = json.load(open(geojson_boundary)).get("features")
    boundary = gpd.GeoDataFrame.from_features(features_bound)

    clip = gpd.clip(data, boundary)

    if not len(clip):
        print("=======")
        print("no data in clip")
        print("=======")
        return
    with open(geojson_output, "w") as f:
        f.write(clip.to_json().encode("utf8").decode())
    # clip.to_file(geojson_output, driver="GeoJSON")
