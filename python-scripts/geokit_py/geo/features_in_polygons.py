"""geo.features_in_polygons: Skeleton of a function."""

import json

from geojson.feature import FeatureCollection as fc
from joblib import Parallel, delayed
from shapely.geometry import shape
from smart_open import open
from tqdm import tqdm


def get_centerid(feature):
    """Return feature center."""
    if not feature.get("geo"):
        feature["geo"] = shape(feature["geometry"])
    return feature["geo"].centroid


def set_shape_feature(features_):
    """Add shape in geo field (featurecollection)"""

    def set_shape(feature):
        """Add shape in geo field (feature)"""
        feature["geo"] = shape(feature["geometry"])
        feature["area"] = feature["geo"].area
        return feature

    new_features = Parallel(n_jobs=-1)(
        delayed(set_shape)(feature)
        for feature in tqdm(features_, desc="Setting 'geo' field")
    )

    return new_features


def filter_include(polygon_features, features, tags_polygon, mode_filter):
    """Filter include (featurecollection)"""

    def filter_include_feature(polygon_features_, feature, tags_polygon_, mode_filter_):
        """Filter feature (feature)"""
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
        for feature in tqdm(features, desc="filter mode : include ")
    )
    return new_feature_includes


def filter_intersects(polygon_features, features, tags_polygon, mode_filter):
    """Filter intersects (featurecollection)"""

    def filter_intersect_feature(
        polygon_features_, feature, tags_polygon_, intersects_range_
    ):
        """Filter intersects (feature)"""
        feature_geo = feature.get("geo")
        for p_f in polygon_features_:
            if p_f["geo"].intersects(feature_geo) or p_f["geo"].contains(feature_geo):
                intersect_feature = p_f["geo"].intersection(feature_geo).area
                p_area = int((intersect_feature / feature["area"]) * 100)
                if p_area >= intersects_range_ or p_f["geo"].contains(feature_geo):
                    feature["properties"]["_where"] = "inside"
                    prop_polygon = p_f["properties"]
                    for t_p in tags_polygon_:
                        feature["properties"][t_p] = prop_polygon.get(t_p, "")
                    return feature
        return feature

    intersects_range = int(mode_filter.split("__")[1])
    new_feature_includes = Parallel(n_jobs=-1)(
        delayed(filter_intersect_feature)(
            polygon_features, feature, tags_polygon, intersects_range
        )
        for feature in tqdm(
            features, desc=f"filter mode : intersects  {intersects_range}"
        )
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
    mode_output: [merged, by_location, by_polygon_tag]
    """

    with open(geojson_in_polygon, encoding="utf8") as gfile:
        polygon_features_ = json.load(gfile).get("features", [])
    with open(geojson_in_features, encoding="utf8") as gfile:
        features_ = json.load(gfile).get("features", [])

    polygon_features = set_shape_feature(polygon_features_)
    features = set_shape_feature(features_)

    for i in features:
        i["properties"]["_where"] = "outside"

    # mode
    features_filter = []
    if "include" in mode_filter:
        features_filter = filter_include(
            polygon_features, features, tags_polygon, mode_filter
        )
    elif "intersect" in mode_filter:
        features_filter = filter_intersects(
            polygon_features, features, tags_polygon, mode_filter
        )

    # remove geo field
    for i in features_filter:
        for j in ["geo", "area"]:
            if j in i.keys():
                del i[j]

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
            geojson_out_features.replace(".geojson", "__where__outside.geojson"), "w"
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
                geojson_out_features.replace(".geojson", "__where__inside.geojson"),
                "w",
            ) as out_geo:
                out_geo.write(
                    json.dumps(fc(data_inside), ensure_ascii=False)
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
