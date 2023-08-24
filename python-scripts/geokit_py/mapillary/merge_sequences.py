"""mapillary.merge_sequences: Skeleton of a function."""

import json

from geojson.feature import FeatureCollection as fc
from joblib import Parallel, delayed
from shapely.geometry import MultiLineString, mapping, shape
from tqdm import tqdm

from geokit_py.utils.map_utils import check_geometry, read_geojson


def get_duplicates(list_):
    """filter duplicates values in a list

    Args:
        list_ (list): list of str
    """
    return list(dict.fromkeys(list(set([x for x in list_ if list_.count(x) > 1]))))


def filter_data_duplicate(features_dict):
    """Function to run in parallel mode to filter duplicate features and merge

    Args:
        features_dict (fc): Dict of features objects
    """

    def merge_data(same_):
        """Merge geometry

        Args:
            same_ (fc): feature object (point)
        """
        try:
            same_shp = [shape(i["geometry"]) for i in same_]
            same_shp_line = [i for i in same_shp if i.geom_type == "LineString"]
            same_shp_multi_line = [
                i for i in same_shp if i.geom_type == "MultiLineString"
            ]
            for multi_line in same_shp_multi_line:
                for line in multi_line:
                    same_shp_line.append(line)

            coords = MultiLineString(same_shp_line)
            data_new = same_[0]
            data_new["geometry"] = mapping(coords)
            return data_new
        except Exception as ex:
            return None

    new_features_duplicates = Parallel(n_jobs=-1)(
        delayed(merge_data)(same_)
        for id_, same_ in tqdm(list(features_dict.items()), desc="merge lines")
    )
    return [i for i in new_features_duplicates if i]


def extra_data(features):
    """Function to run in parallel mode to add extra fields

    Args:
        features (fc): List of features objects
    """

    def add_extra_data(feature_):
        """Add extra fields in properties from geometry

        Args:
            feature_ (dict): feature object
        """
        geom_shape = shape(feature_["geometry"])
        feature_["properties"]["length"] = geom_shape.length
        feature_["properties"]["points"] = (
            sum([len(i.coords) for i in geom_shape])
            if geom_shape.geom_type == "MultiLineString"
            else len(geom_shape.coords)
        )
        return feature_

    new_features = Parallel(n_jobs=-1)(
        delayed(add_extra_data)(feature)
        for feature in tqdm(features, desc="add extra data")
    )
    return new_features


def merge_sequences(geojson_input, geojson_output):
    """Start processing sequence geojson files

    Args:
        geojson_input (str): Pathfile for geojson input
        geojson_output (str): Pathfile for geojson output
    """
    features = read_geojson(geojson_input)
    features = [i for i in features if check_geometry(i)]

    initial_objects = len(features)
    id_duplicates = get_duplicates(
        [
            i["properties"].get("sequence_id")
            for i in features
            if i["properties"].get("sequence_id")
        ]
    )

    list_no_duplicates = []
    list_duplicates = {}
    for feature in features:
        fake_id = feature["properties"]["sequence_id"]
        feature["properties"]["id"] = fake_id

        if fake_id in id_duplicates:
            if fake_id in list_duplicates.keys():
                list_duplicates[fake_id].append(feature)
            else:
                list_duplicates[fake_id] = [
                    feature,
                ]
        else:
            list_no_duplicates.append(feature)

    # liberate memory
    del features
    new_features_duplicates = filter_data_duplicate(list_duplicates)
    merge_lines = [*list_no_duplicates, *new_features_duplicates]

    merge_lines_extra = extra_data(merge_lines)

    print("==========")
    print("initial_objects ", initial_objects)
    print("total_objects ", len(merge_lines_extra))
    json.dump(fc(merge_lines_extra), open(geojson_output, "w"))
