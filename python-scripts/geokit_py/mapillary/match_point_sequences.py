"""mapillary.match_point_sequences: Skeleton of a function."""

import json
import logging

from geojson.feature import FeatureCollection as fc
from joblib import Parallel, delayed
from tqdm import tqdm

from geokit_py.utils.map_utils import geom_data

logger = logging.getLogger("__name__")


def poly_in_point(features, features_poly):
    """Function to run in parallel mode to filter points in polygon geometry

    Args:
        features (fc): List of features objects (points)
        features_poly (fc): List of features objects (polygons)
    """

    def feature_in_seq(feature_, features_poly_):
        """Filter a point into a polygon

        Args:
            feature_ (dict): feature object (point)
            features_poly_ (dict): List of features objects (polygons)
        """
        feature_shape = feature_["geom"]
        feature_seq = feature_["properties"]["sequence_id"]
        for feature_poly in features_poly_:
            feature_poly_shape = feature_poly["geom"]
            feature_poly_seq = feature_poly["properties"]["sequence_id"]
            if feature_seq == feature_poly_seq:
                if feature_poly_shape.intersects(feature_shape):
                    return feature_
        return None

    new_features = Parallel(n_jobs=-1, prefer="threads")(
        delayed(feature_in_seq)(feature, features_poly)
        for feature in tqdm(features, desc="points in polygons")
    )
    return [i for i in new_features if i]


def match_point_sequences(geojson_polygons, geojson_points, geojson_output):
    """Start to filter point in polygons and and secuence_id

    Args:
        geojson_polygons (str):  Pathfile for geojson input (polygons)
        geojson_points (str):  Pathfile for geojson input (points)
        geojson_output (str):  Pathfile for geojson output (points)
    """

    features_poly = geom_data(json.load(open(geojson_polygons)).get("features"))
    features_points = geom_data(json.load(open(geojson_points)).get("features"))
    list_sequences = list([i["properties"]["sequence_id"] for i in features_poly])
    points_in_dequence = list(
        [i for i in features_points if i["properties"]["sequence_id"] in list_sequences]
    )

    filter_data = poly_in_point(points_in_dequence, features_poly)
    # remove points duplicates
    points_dict = {str(i["geom"].wkb_hex): i for i in filter_data}
    filter_data = list(points_dict.values())
    for i in filter_data:
        if "geom" in i.keys():
            del i["geom"]
    print("==========")
    print("initial points ", len(features_points))
    print("points in sequence ", len(points_in_dequence))
    print("Points filter (spatial - seq) ", len(filter_data))
    json.dump(fc(filter_data), open(geojson_output, "w"))
