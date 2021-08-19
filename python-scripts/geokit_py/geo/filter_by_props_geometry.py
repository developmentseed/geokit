"""geo.filter_by: Skeleton of a function."""

import json

from geojson.feature import FeatureCollection as fc
from smart_open import open


def filter_props(features, props_filter, is_strict):
    """Filter by props (feturecollection)."""

    def filter_props_feature(feature_, props_filter_, is_strict_):
        """Filter by geometry (feature)."""

        feature_props = feature_.get("properties", {})
        flags = []
        for i in props_filter_:
            key, value = i.strip().split("=")
            if feature_props.get(key) is not None:
                if value == "*":
                    flags.append(True)
                elif str(feature_props.get(key)) == str(value):
                    flags.append(True)
                else:
                    flags.append(False)
            else:
                flags.append(False)
        if is_strict_:
            if all(flags):
                return feature_
        else:
            if any(flags):
                return feature_
        return None

    new_feature_includes = [
        filter_props_feature(feature, props_filter, is_strict) for feature in features
    ]
    return [i for i in new_feature_includes if i]


def filter_geometry(features, props_filter):
    """Filter by geometry."""
    new_feature_includes = []
    for feature in features:
        feature_type = str(feature["geometry"].get("type"))
        if feature_type in props_filter:
            new_feature_includes.append(feature)
    return new_feature_includes


def filter_by(geojson_input, props, mode_filter, mode_output, geojson_output, is_test):
    """
    Difference between two geojson files according to an attribute
    """
    with open(geojson_input, "r", encoding="utf8") as gfile:
        json_data = json.load(gfile).get("features", [])

    if mode_filter == "by_geometry":
        for prop in props:
            if "=" in prop:
                raise Exception("In geometry mode = not necessary")
            if prop not in [
                "Point",
                "LineString",
                "Polygon",
                "MultiPoint",
                "MultiLineString",
                "MultiPolygon",
            ]:
                raise Exception(
                    "The geometry its no valid, the options are : \n"
                    " Point, LineString, Polygon, MultiPoint, MultiLineString and MultiPolygon"
                )
        features_filter = filter_geometry(json_data, props)

    else:
        # validate ops
        for prop in props:
            if "=" not in prop:
                raise Exception(f"The property '{prop}' does not have the = symbol")
            if not len(prop.split("=")) == 2:
                raise Exception(
                    f"The property '{prop}' does not have the form key=value"
                )

        features_filter = filter_props(json_data, props, "strict" in mode_filter)

    # output - modes
    print("================")
    print(f"Original  : {str(len(json_data)).zfill(3)} features")
    print(f"Filtered  : {str(len(features_filter)).zfill(3)} features")

    if is_test:
        return features_filter

    if mode_output == "merged":
        with open(geojson_output, "w") as out_geo:
            out_geo.write(
                json.dumps(fc(features_filter), ensure_ascii=False)
                .encode("utf8")
                .decode()
            )

    if mode_output == "by_props":
        print("====== STATS ==========")
        if mode_filter == "by_geometry":
            raise Exception("incongruity, mode_filter = by_geometry")
        for prop in props:
            key, value = prop.strip().split("=")
            data = [i for i in features_filter if i["properties"].get(key) is not None]
            print(f"{key}: {value}  => {len(data)} features")
            with open(
                geojson_output.replace(".geojson", f"__{key}__{value}.geojson"), "w"
            ) as out_geo:
                out_geo.write(
                    json.dumps(fc(data), ensure_ascii=False).encode("utf8").decode()
                )
    if mode_output == "by_geometry":
        print("====== STATS ==========")
        if not mode_filter == "by_geometry":
            raise Exception("incongruity, mode_filter its not by_geometry")
        for geometry in props:
            data = [i for i in features_filter if i["geometry"]["type"] == geometry]
            print(f"geometry: {geometry}  => {len(data)} features")
            with open(
                geojson_output.replace(".geojson", f"__geometry__{geometry}.geojson"),
                "w",
            ) as out_geo:
                out_geo.write(
                    json.dumps(fc(data), ensure_ascii=False).encode("utf8").decode()
                )
