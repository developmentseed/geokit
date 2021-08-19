"""
Author: @developmentseed
"""

import json

import affine
import shapely
from geojson import Feature
from geojson import FeatureCollection as fc
from shapely.geometry import Point, box, mapping, shape
from smart_open import open


def pixel2geo_point(feature):
    """return Point from pixel."""
    geom = shape(feature["geometry"])
    pointScale = feature["properties"]["pointScale"]
    pxbox = 0, 0, pointScale["x"], pointScale["y"]
    bnds = geom.bounds
    width = bnds[2] - bnds[0]
    height = bnds[3] - bnds[1]
    a = affine.Affine(width / 256, 0.0, bnds[0], 0.0, (0 - height / 256), bnds[3])
    a_lst = [a.a, a.b, a.d, a.e, a.xoff, a.yoff]
    poly = shapely.affinity.affine_transform(box(*pxbox), a_lst)
    bounds = poly.bounds
    point = Point(bounds[2], bounds[1])
    new_feature = Feature(properties=feature["properties"], geometry=mapping(point))
    return new_feature


def center_tile(feature):
    """Return feature center."""
    geom = shape(feature["geometry"])
    point = geom.centroid
    new_feature = Feature(properties=feature["properties"], geometry=mapping(point))
    return new_feature


def filter_chips(geojson_file, geojson_output):
    """Run scrip."""
    with open(geojson_file, encoding="utf8") as gfile:
        features = json.load(gfile).get("features", [])
    features_yes = [
        dict(feature)
        for feature in features
        if feature["properties"].get("_has_school") == "yes"
    ]
    features_no = [
        dict(feature)
        for feature in features
        if feature["properties"].get("_has_school") == "no"
    ]
    features_no_point = [
        center_tile(feature)
        for feature in features
        if feature["properties"].get("_has_school") == "no"
    ]
    features_yes_point = [
        pixel2geo_point(feature)
        for feature in features_yes
        if feature["properties"].get("pointScale")
    ]
    geojson_output_yes_point = geojson_output.replace(".geojson", "__yes_point.geojson")
    with open(geojson_output_yes_point, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features_yes_point), ensure_ascii=False)
            .encode("utf8")
            .decode()
        )

    geojson_output_yes = geojson_output.replace(".geojson", "__yes_tile.geojson")
    with open(geojson_output_yes, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features_yes), ensure_ascii=False).encode("utf8").decode()
        )

    geojson_output_no = geojson_output.replace(".geojson", "__no_tile.geojson")
    with open(geojson_output_no, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features_no), ensure_ascii=False).encode("utf8").decode()
        )
    geojson_output_no_point = geojson_output.replace(".geojson", "__no_point.geojson")
    with open(geojson_output_no_point, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features_no_point), ensure_ascii=False)
            .encode("utf8")
            .decode()
        )

    print(f"yes_tile => {len(features_yes)}")
    print(f"no_tile => {len(features_no)}")
