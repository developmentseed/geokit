"""geo.features_in_polygons: Skeleton of a function."""

import json
from uuid import uuid1

from geojson.feature import FeatureCollection as fc, Feature
from smart_open import open
from shapely.geometry import geo, Point, shape
from joblib import Parallel, delayed
from tqdm import tqdm


def get_centerid(feature):
    """Return feature center."""
    if not feature.get("geo"):
        feature["geo"] = shape(feature["geometry"])
    return feature["geo"].centroid


def set_shape_feature(features_):
    def set_shape(feature):
        feature["geo"] = shape(feature["geometry"])
        return feature

    new_features = Parallel(n_jobs=-1)(
        delayed(set_shape)(feature)
        for feature in tqdm(features_, desc=f"Setting 'geo' field")
    )

    return new_features


def filter_include(polygon_features, features, tags_polygon, mode_filter):
    def filter_include_feature(polygon_features_, feature, tags_polygon_, mode_filter_):
        for p_f in polygon_features_:
            feature_geo = (
                feature["geo"].centroid
                if "centroid" in mode_filter_
                else feature["geo"]
            )

            if p_f["geo"].contains(feature_geo):
                feature["properties"]["_where"] = "inside"
                prop_polygon = p_f["properties"]
                for t_p in tags_polygon_:
                    feature["properties"][t_p] = prop_polygon.get(t_p, "")
                return feature
        return feature

    new_feature_includes = Parallel(n_jobs=-1)(
        delayed(filter_include_feature)(
            polygon_features, feature, tags_polygon, mode_filter
        )
        for feature in tqdm(features, desc=f"filter mode : include ")
    )
    return new_feature_includes


def features_in_polygons(
    geojson_in_polygon: str,
    geojson_in_features: str,
    tags_polygon: list,
    mode_filter: str,
    mode_output: str,
    geojson_out_features: str,
):
    """Script for add tag in feature (included).
    mode_filter: [include, include__centroid]
    mode_filter: [normal , where and tags_polygon]

    """

    with open(geojson_in_polygon, encoding="utf8") as gfile:
        polygon_features_ = json.load(gfile).get("features", [])
    with open(geojson_in_features, encoding="utf8") as gfile:
        features_ = json.load(gfile).get("features", [])

    polygon_features = set_shape_feature(polygon_features_)
    features = set_shape_feature(features_)

    # check polygon_features its polygon
    if not all(["Polygon" in g["geo"].geom_type for g in polygon_features]):
        raise Exception("have a geojson in polygon it's not a polygon")
    #  all features are outside
    for i in features:
        i["properties"]["_where"] = "outside"

    # mode
    features_filter = []
    if "include" in mode_filter:
        features_filter = filter_include(
            polygon_features, features, tags_polygon, mode_filter
        )

    # remove geo field
    for i in features_filter:
        if "geo" in i.keys():
            del i["geo"]

    # output - modes
    print("================")
    print(f"Total  : {len(features_filter)} features")
    print("====== STATS ==========")

    if mode_output == "merged":
        with open(geojson_out_features, "w") as out_geo:
            out_geo.write(
                json.dumps(fc(features_filter), ensure_ascii=False)
                .encode("utf8")
                .decode()
            )
    else:
        # save outside
        data_outside = [
            i for i in features_filter if i["properties"]["_where"] == "outside"
        ]
        with open(
            geojson_out_features.replace(".geojson", f"__where__outside.geojson"), "w"
        ) as out_geo:
            out_geo.write(
                json.dumps(fc(data_outside), ensure_ascii=False).encode("utf8").decode()
            )
        print(f"_where: outside  => {len(data_outside)} features")

        if mode_output == "by_location":
            data_inside = [
                i for i in features_filter if i["properties"]["_where"] == "inside"
            ]
            with open(
                geojson_out_features.replace(".geojson", f"__where__inside.geojson"),
                "w",
            ) as out_geo:
                out_geo.write(
                    json.dumps(fc(data_outside), ensure_ascii=False)
                    .encode("utf8")
                    .decode()
                )
            print(f"_where: inside  => {len(data_inside)} features")

        if mode_output == "by_polygon_tag":
            if not tags_polygon:
                raise Exception(
                    "incongruity, need tags_polygon to save in this mode_output"
                )
            for tag_polygon in tags_polygon:
                value_tags = list(
                    dict.fromkeys(
                        [
                            i["properties"].get(tag_polygon)
                            for i in features_filter
                            if i["properties"]["_where"] == "inside"
                            and i["properties"].get(tag_polygon, False)
                        ]
                    )
                )
                for val in value_tags:
                    data = [
                        i
                        for i in features_filter
                        if i["properties"]["_where"] == "inside"
                        and i["properties"].get(tag_polygon, "") == val
                    ]
                    print(f"{tag_polygon}: {val}  => {len(data)} features")
                    with open(
                        geojson_out_features.replace(
                            ".geojson", f"__{tag_polygon}__{val}.geojson"
                        ),
                        "w",
                    ) as out_geo:
                        out_geo.write(
                            json.dumps(fc(data), ensure_ascii=False)
                            .encode("utf8")
                            .decode()
                        )
