"""utils.map_utils: Skeleton of a function."""

import json
import os
import random
from itertools import chain

import mercantile
import requests
from geojson import FeatureCollection
from joblib import Parallel, delayed
from shapely.geometry import shape
from smart_open import open
from tqdm import tqdm
from vt2geojson.tools import vt_bytes_to_geojson

access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")


def get_mapillary_points_bbox(
    bbox, only_pano=True, timestamp_from=0, geom=None, name_file=""
):
    """Get a bbox and returns a feature list of mapillary points that are pano images

    Args:
        bbox (tuple): bounds area to get the points
        only_pano (bool): flag to filter pano points
        timestamp_from (int): date in timestamp to filter
        geom (object): geometry from shapely
        name_file (str): file name for description
    Returns:
        list: list of features
    """

    def filter_feature(feature_, bbox_, geom_, only_pano_, timestamp_from_):
        """Run in parallel"""
        west, south, east, north = bbox_

        lng = feature_["geometry"]["coordinates"][0]
        lat = feature_["geometry"]["coordinates"][1]
        # conditional cases
        conditional = True
        if only_pano_:
            conditional = feature_["properties"]["is_pano"]
        if timestamp_from_:
            conditional = conditional and bool(
                int(feature_["properties"]["captured_at"]) >= timestamp_from_
            )
        if geom_:
            if conditional and geom_.contains(shape(feature_["geometry"])):
                return feature_
            return None
        elif lng > west and lng < east and lat > south and lat < north and conditional:
            return feature_
        return None

    mapillary_URL = (
        "https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}&"
    )
    tile_coverage = "mly1_public"
    tile_layer = "image"
    west, south, east, north = bbox
    tiles = list(mercantile.tiles(west, south, east, north, 14))
    features = []
    for tile in tqdm(tiles, desc=f"download data {name_file}"):
        tile_url = mapillary_URL.format(
            tile_coverage, tile.z, tile.x, tile.y, access_token
        )
        response = requests.get(tile_url)
        data = vt_bytes_to_geojson(
            response.content, tile.x, tile.y, tile.z, layer=tile_layer
        )
        # Filter pano images in the area
        features_tmp = Parallel(n_jobs=-1, prefer="threads")(
            delayed(filter_feature)(feature_, bbox, geom, only_pano, timestamp_from)
            for feature_ in data["features"]
        )
        # clean features
        features_tmp = [i for i in features_tmp if i]
        features.append(features_tmp)

    return list(chain.from_iterable(features))


def build_mapillary_sequence(points, fetch_points=False):
    """Build sequence  using points, return linestring

    Args:
        points (fc): Feature collection of points

    Returns:
        list[fc]: Feature collection of linestring
    """
    sequences = {}
    points_sorted = sorted(
        points, key=lambda item: int(item["properties"]["captured_at"])
    )
    for point in points_sorted:
        sequence_id = str(point["properties"]["sequence_id"])
        id = str(point["properties"]["id"])

        if sequence_id not in sequences.keys():
            sequences[sequence_id] = {
                "type": "Feature",
                "properties": {
                    "sequence_id": sequence_id,
                    "is_pano": point["properties"]["is_pano"],
                    "images_id": [],
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [],
                },
            }
        sequences[sequence_id]["geometry"]["coordinates"].append(
            point["geometry"]["coordinates"]
        )
        sequences[sequence_id]["properties"]["images_id"].append(id)
    sequences = list(sequences.values())
    for seq in sequences:
        seq["properties"]["total_points"] = seq["geometry"]["coordinates"].__len__()
        images_id = list(seq["properties"]["images_id"])
        step = int(len(images_id) * 10 / 100)
        if step < 10:
            step = 1
        seq["properties"]["images_id"] = ",".join(
            [
                i
                for (k, i) in enumerate(images_id)
                if k in list(range(0, len(images_id), step))
            ]
        )

    if fetch_points:
        header = {"Authorization": f"OAuth {access_token}"}

        def fetch_url_images(feature):
            feature["properties"]["custom_url"] = ""
            feature["properties"]["custom_urls"] = ""

            try:
                total_images_list = feature["properties"].get("images_id").split(",")
                if len(total_images_list) <= 5:
                    images_filter = total_images_list
                else:
                    images_filter = list(
                        dict.fromkeys(list(random.sample(total_images_list, 5)))
                    )

                list_urls = []

                for image_ in images_filter:
                    try:
                        url = "https://graph.mapillary.com/{}?fields=thumb_1024_url".format(
                            image_
                        )
                        r = requests.get(url, headers=header, timeout=5)
                        data = r.json()
                        list_urls.append(data["thumb_1024_url"])
                    except Exception as ex_:
                        print("ex_", ex_)

                image_select = random.choice(list_urls)
                feature["properties"]["custom_url"] = image_select
                feature["properties"]["custom_urls"] = ",".join(
                    [i for i in list_urls if i != image_select]
                )
            except Exception as ex:
                print("ex", ex)
            return feature

        new_sequences = Parallel(n_jobs=-1)(
            delayed(fetch_url_images)(feature)
            for feature in tqdm(sequences, desc="download images")
        )
        sequences = new_sequences

    return list(sequences)


def read_geojson(input_file):
    """Read a geojson file and return a list of features

    Args:
        input_file (str): Location of geojson file

    Returns:
        list: list fo features
    """
    fc = []
    with open(input_file, "r", encoding="utf8") as f:
        cf = json.load(f)["features"]
    return cf


def write_geojson(output_file, list_features):
    """Write geojson files

    Args:
        output_file (str): Location of ouput file
        list_features (list): List of features
    """
    with open(output_file, "w") as f:
        json.dump(FeatureCollection(list_features), f)


def check_geometry(feature):
    """Verify if geometry is valid

    Args:
        feat (obj): Feature

    Returns:
        Bool: Return false or true acoording to the geometry
    """
    try:
        geom_shape = shape(feature["geometry"])
        return geom_shape.is_valid
    except Exception:
        return False


def geom_data(features):
    """Function to run in parallel mode to add shapely geometry

    Args:
        features (fc): List of features objects
    """

    def geom_data_feat(feature_):
        """Add shapely geometry in feature

        Args:
            feature_ (dict): feature object
        """
        geom_shape = shape(feature_["geometry"])
        feature_["geom"] = geom_shape
        return feature_

    new_features = Parallel(n_jobs=-1)(
        delayed(geom_data_feat)(feature) for feature in tqdm(features, desc="geom data")
    )
    return new_features


def validate_output_path(file_path):
    """Function to validate the file, if it is geojson file, and create the folder if it doesn't exist
    Args:
        file_path: File path
    Returns:
        Bool: Return True if both validations were successful.
    """
    expected_extension = ".geojson"

    file_name = os.path.basename(file_path)

    if "/" not in file_path:
        file_path = os.path.join(os.getcwd(), file_name)

    if not file_name.lower().endswith(expected_extension):
        print("Error: Enter output file with geojson extension")
        return False

    folder_path = os.path.dirname(file_path)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

    return True
