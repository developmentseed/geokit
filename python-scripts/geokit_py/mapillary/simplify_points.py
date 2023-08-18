import click
import random
from geokit_py.utils.map_utils import read_geojson, write_geojson, geom_data

from copy import deepcopy
from shapely.geometry import Point

import pyproj


def transform_projection(point, src_proj, dst_proj):
    transformer = pyproj.Transformer.from_proj(src_proj, dst_proj, always_xy=True)
    x, y = transformer.transform(point[0], point[1])
    p = Point(x, y)
    return p


def distance(point1, point2):
    """calculate the distance between two points

    Args:
        point1 (geom): feature object (point)
        point2 (geom): feature object (point)
    """
    dist = point1.distance(point2)
    return dist


def simplify_points(input_points, points_distance, output_points):
    features = read_geojson(input_points)
    features = geom_data(features)
    sequences = {}

    # Sort by sequence id
    for feature in features:
        sequence_id = str(feature["properties"]["sequence_id"])
        point_new_coord = transform_projection(
            feature["geometry"]["coordinates"], "epsg:4326", "epsg:3857"
        )
        feature["new_point"] = point_new_coord
        if sequence_id not in sequences.keys():
            sequences[sequence_id] = []
        sequences[sequence_id].append(feature)

    base = None
    filter_points = []
    for sequence in sequences.values():
        points_sorted = sorted(
            sequence, key=lambda item: int(item["properties"]["captured_at"])
        )
        for point in points_sorted:
            if base is None:
                base = point
                filter_points.append(deepcopy(base))
                continue

            d = distance(base["new_point"], point["new_point"])
            if d >= float(points_distance):
                filter_points.append(deepcopy(point))
                base = point

    for i in filter_points:
        if "geom" in i.keys():
            del i["geom"]
            del i["new_point"]

    print("Simplify points")
    print("initial data", len(features))
    print("result data", len(filter_points))
    print("=======")
    write_geojson(output_points, filter_points)
