"""mapillary.simplify_sequence: Skeleton of a function."""
import json

from geojson.feature import FeatureCollection as fc
from joblib import Parallel, delayed
from shapely.geometry import mapping, shape
from tqdm import tqdm


def is_include(geom_a, geom_b):
    """Determines if two polygons are included

    Args:
        geom_a (shape): geometries of the first polygon
        geom_b (shape): geometries of the second polygon
    """
    return geom_a.contains(geom_b) or geom_b.contains(geom_a)


def shp_data(features, buffer):
    """Function to run in parallel mode to add shapely geometry

    Args:
        features (fc): List of features objects
    """

    def shp_data_feat(feature_, buffer_):
        """Add shapely geometry in feature

        Args:
            feature_ (dict): feature object
        """
        geom_shape = shape(feature_["geometry"])

        shp_buff = geom_shape.buffer(buffer_)
        feature_["geom"] = shp_buff
        feature_["properties"]["area"] = (
            shp_buff.area
            if shp_buff.geom_type == "Polygon"
            else sum([pol.area for pol in shp_buff])
        )
        feature_["id"] = feature_["properties"].get("id")
        return feature_

    new_features = Parallel(n_jobs=-1)(
        delayed(shp_data_feat)(feature, buffer)
        for feature in tqdm(features, desc="shp data")
    )
    return list(sorted(new_features, key=lambda x: -x["properties"].get("length")))


def find_intersection_override(features):
    """Filter features by area, add is_exclude field

    Args:
        features (fc): List of features objects
    """

    for idx_ in tqdm(range(len(features)), desc="filter by area "):
        feature_ = features[idx_]
        geom_feature = feature_["geom"]

        if not geom_feature.is_valid or ("Polygon" not in geom_feature.geom_type):
            feature_["properties"]["is_exclude"] = True

        is_exclude = feature_["properties"].get("is_exclude")

        ids_intersect = feature_.get("properties").get("intersects")
        ids_contains = []
        if not is_exclude:
            area = geom_feature.area

            for feat_menor in features[idx_ + 1 :]:
                feat_menor_id = feat_menor.get("id")
                # only intersetcs previus filter
                if feat_menor_id not in ids_intersect:
                    continue
                if feat_menor["properties"].get("is_exclude"):
                    continue

                geom_menor = feat_menor["geom"]

                if "Polygon" not in geom_menor.geom_type:
                    feat_menor["properties"]["is_exclude"] = True
                    continue

                try:
                    if geom_feature.intersects(geom_menor):
                        if geom_feature.contains(geom_menor):
                            feat_menor["properties"]["is_exclude"] = True
                            ids_contains.append(feat_menor["id"])
                        else:
                            difference = geom_menor.difference(geom_feature)
                            feat_menor["geom"] = difference
                            if not difference.is_valid:
                                feat_menor["properties"]["is_exclude"] = True
                                continue
                except Exception as ex:
                    print(ex.__str__())
                    feat_menor["properties"]["is_exclude"] = True
            feature_["properties"]["contains"] = ids_contains

    return features


def remove_include(features):
    """Function to run in parallel mode to remove features that have been included

    Args:
        features (fc): List of features objects
    """

    def filter_include(features_, feature_):
        """Remove feature its include in another geometry

        Args:
            features_ (fc): List of features objects
            feature_ (dict): feature object
        """
        geom_feat = feature_["geom"]
        is_include_ = any(
            [is_include(other_feat["geom"], geom_feat) for other_feat in features_]
        )
        if not is_include_:
            return feature_
        return None

    new_features = Parallel(n_jobs=-1, prefer="threads")(
        delayed(filter_include)(features[idx + 1 :], features[idx])
        for idx in tqdm(list(range(len(features))), desc="remove includes")
    )
    return [i for i in new_features if i]


def group_intersects(features):
    """Function to run in parallel mode to add a field with all the features it intersects

    Args:
        features (fc): List of features objects
    """

    def filter_intersetcs(features_, feature_):
        """Adds a field with all the features it intersects

        Args:
            features_ (fc): List of features objects
            feature_ (dict): feature
        """
        geom_feat = feature_["geom"]
        id = feature_.get("id")
        intersetcs = []
        for other_feature in features_:
            id_other = other_feature.get("id")
            if id != id_other and other_feature["geom"].intersects(geom_feat):
                intersetcs.append(id_other)
        feature_["properties"]["intersects"] = intersetcs
        feature_["properties"]["has_intersects"] = intersetcs.__len__() > 0

        return feature_

    new_features = Parallel(n_jobs=-1, prefer="threads")(
        delayed(filter_intersetcs)(features, feature)
        for feature in tqdm(features, desc="group intersects")
    )
    return new_features


def simplify_sequence(geojson_input, buffer, geojson_out):
    """Start the line simplification process

    Args:
        geojson_input (str):  Pathfile for geojson input
        geojson_out (str):  Pathfile for geojson output
    """
    features = json.load(open(geojson_input, "r")).get("features")
    stats = {"original size": len(features)}
    features = shp_data(features, buffer)
    # features no include
    features = remove_include(features)
    stats["features no include"] = len(features)
    # add intersetcs field
    features = group_intersects(features)
    features_no_intersetcs = []
    features_has_intersetcs = []
    for i in features:
        if i["properties"]["has_intersects"]:
            features_has_intersetcs.append(i)
        else:
            features_no_intersetcs.append(i)
    stats["features no intersects"] = len(features_no_intersetcs)

    data = find_intersection_override(features)

    data_compile = [*data, *features_no_intersetcs]
    data_filter = []
    # clean data
    for i in data_compile:
        if "geom" in i.keys():
            geom = i["geom"]
            if "Polygon" in geom.geom_type:
                i["geometry"] = mapping(i["geom"])
                del i["geom"]
                data_filter.append(i)
    stats["features filtered "] = len(data_filter)
    json.dump(fc(data_filter), open(geojson_out, "w"))
    print("===================")
    for k, v in stats.items():
        print(f"{k} : {v}")
