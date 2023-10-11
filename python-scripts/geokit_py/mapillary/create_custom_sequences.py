"""mapillary.create_custom_sequences: Skeleton of a function."""

import json

from geokit_py.utils.map_utils import build_mapillary_sequence, write_geojson


def create_custom_sequences(geojson_points, output_file_sequence):
    """Script to add Mapillary's URLs to review the images of the sequences"""
    features = json.load(open(geojson_points)).get("features")
    sequences = build_mapillary_sequence(features, True)
    write_geojson(output_file_sequence, sequences)
