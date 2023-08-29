"""mapillary.download_mapillary_imgs: Skeleton of a function."""

import requests
import os
from joblib import Parallel, delayed
from tqdm import tqdm
from geokit_py.utils.map_utils import read_geojson, write_geojson

access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")


def download_img(feature, output_images_path):
    """Download images from Mapillary

    Args:
        feature (dict): feture
        output_images_path (str): path to save the images
    Returns:
        list: features
    """
    sequence_id = feature["properties"]["sequence_id"]
    image_folder_path = f"{output_images_path}/{sequence_id}"
    new_feature = None
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)

    # request the URL of each image
    image_id = feature["properties"]["id"]

    # Check if mapillary image exist and download
    img_file_equirectangular = f"{image_folder_path}/{image_id}.jpg"
    # img_file_cubemap = f"{image_folder_path}/{image_id}_cubemap.jpg"

    header = {"Authorization": "OAuth {}".format(access_token)}
    url = "https://graph.mapillary.com/{}?fields=thumb_1024_url".format(image_id)

    try:
        r = requests.get(url, headers=header)
        data = r.json()
        image_url = data["thumb_1024_url"]

        with open(img_file_equirectangular, "wb") as handler:
            image_data = requests.get(image_url, stream=True).content
            handler.write(image_data)

    except Exception as ex:
        print(ex)
    # return new_feature
    return feature


def process_image(features, output_images_path):
    """Function to run in parallel mode to process mapillary images

    Args:
        features (fc): List of features objects
        output_images_path (str): Location to save images

    Returns:
        fc: List of points that images were processed
    """
    # Process in parallel
    results = Parallel(n_jobs=-1)(
        delayed(download_img)(feature, output_images_path)
        for feature in tqdm(
            features, desc="Processing images for...", total=len(features)
        )
    )
    return results


def download_mapillary_imgs(
    input_file_points,
    output_images_path,
    output_file_points,
):
    """Script to download Mapillary images"""

    features = read_geojson(input_file_points)
    output = process_image(features, output_images_path)
    features = [fea for fea in output if fea is not None]
    write_geojson(output_file_points, features)
