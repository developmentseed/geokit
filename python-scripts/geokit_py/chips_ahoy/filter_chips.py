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


def clean_feature(features, clean_fields):
    """remove unnecesary fields of featurecollection"""

    if clean_fields:
        remove_fields = ["pointScale", "sizeImage", "__reviewed"]
        for feature in features:
            prop_feature = feature.get("properties")
            prop_feature_fields = prop_feature.keys()
            for field in remove_fields:
                if field in prop_feature_fields:
                    del prop_feature[field]

    return features


def filter_chips(geojson_file, clean_fields, geojson_output):
    """Run scrip."""
    with open(geojson_file, encoding="utf8") as gfile:
        features = json.load(gfile).get("features", [])
    features_yes = [
        dict(feature)
        for feature in features
        if feature["properties"].get("dc_has_pattern_school") == "yes"
    ]
    features_no = [
        dict(feature)
        for feature in features
        if feature["properties"].get("dc_has_pattern_school") == "no"
    ]
    features_no_point = [
        center_tile(feature)
        for feature in features
        if feature["properties"].get("dc_has_pattern_school") == "no"
    ]
    features_yes_point = [
        pixel2geo_point(feature)
        for feature in features_yes
        if feature["properties"].get("pointScale")
    ]
    # save files
    geojson_output_yes_point = geojson_output.replace(".geojson", "__yes_point.geojson")
    with open(geojson_output_yes_point, "w") as out_geo:
        out_geo.write(
            json.dumps(
                fc(clean_feature(features_yes_point, clean_fields)), ensure_ascii=False
            )
            .encode("utf8")
            .decode()
        )

    geojson_output_yes = geojson_output.replace(".geojson", "__yes_tile.geojson")
    with open(geojson_output_yes, "w") as out_geo:
        out_geo.write(
            json.dumps(
                fc(clean_feature(features_yes, clean_fields)), ensure_ascii=False
            )
            .encode("utf8")
            .decode()
        )

    geojson_output_no = geojson_output.replace(".geojson", "__no_tile.geojson")
    with open(geojson_output_no, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(clean_feature(features_no, clean_fields)), ensure_ascii=False)
            .encode("utf8")
            .decode()
        )
    geojson_output_no_point = geojson_output.replace(".geojson", "__no_point.geojson")
    with open(geojson_output_no_point, "w") as out_geo:
        out_geo.write(
            json.dumps(
                fc(clean_feature(features_no_point, clean_fields)), ensure_ascii=False
            )
            .encode("utf8")
            .decode()
        )

    print(f"yes_tile => {len(features_yes)}")
    print(f"no_tile => {len(features_no)}")
