"""utils.utils_images: Skeleton of a function."""

import glob
import os
from pathlib import Path

import cv2
import requests
from joblib import Parallel, delayed
from PIL import Image
from smart_open import open
from tqdm import tqdm

access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")


def cubemap_splitter(
    img_file_cubemap,
    image_clip_size,
    sequence_id,
    image_id,
    output_images_path,
    cube_sides,
):
    """Split cubemap images

    Args:
        img_file_cubemap (str): Location of cubemap image
        image_clip_size (int): Size of the image to clip
        sequence_id (str): Mapillary sequece id
        image_id (ssstr): Mapillary img id
        output_images_path (str): Location to save the images
        cube_sides (str): Sides to processes the image
    """
    img = cv2.imread(img_file_cubemap)
    img_height = img.shape[0]
    img_width = img.shape[1]
    r = img_width - img_height
    h = w = image_clip_size
    horizontal_chunks = 4
    vertical_chunks = 3
    index_dict = {
        "1,0": "top",
        "0,1": "left",
        "1,1": "front",
        "2,1": "right",
        "3,1": "back",
        "1,2": "bottom",
    }
    sides = cube_sides.split(",")
    for x in range(0, horizontal_chunks):
        for y in range(0, vertical_chunks):
            index = f"{x},{y}"
            if index in index_dict.keys() and index_dict[index] in sides:
                crop_img = img[y * r : y * r + h, x * r : x * r + w]
                imageRGB = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
                img_ = Image.fromarray(imageRGB, mode="RGB")
                chunk_img_path = f"{output_images_path}/{sequence_id}/{image_id}_{index_dict[index]}.jpg"
                with open(chunk_img_path, "wb") as sfile:
                    img_.save(sfile)
                    print(f"Saving...{chunk_img_path}")


def download_clip_img(feature, output_images_path, image_clip_size, cube_sides):
    """Download and clip the spherical image

    Args:
        feature (dict): feture
        output_images_path (str): path to save the images
        image_clip_size (int): Size of the image to clip
        cube_sides (string): sides to process images
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
    img_file_cubemap = f"{image_folder_path}/{image_id}_cubemap.jpg"

    header = {"Authorization": "OAuth {}".format(access_token)}
    url = "https://graph.mapillary.com/{}?fields=thumb_1024_url".format(image_id)

    try:
        r = requests.get(url, headers=header)
        data = r.json()
        image_url = data["thumb_1024_url"]

        with open(img_file_equirectangular, "wb") as handler:
            image_data = requests.get(image_url, stream=True).content
            handler.write(image_data)

        # Convert Equirectangular -> Cubemap
        cmd = f"convert360 --convert e2c --i {img_file_equirectangular}  --o {img_file_cubemap} --w {image_clip_size}"
        os.system(cmd)

        # Split Cubemap to simple images
        chumk_image_path = f"{image_folder_path}/{image_id}"
        if not os.path.exists(chumk_image_path):
            os.makedirs(chumk_image_path)
        cubemap_splitter(
            img_file_cubemap,
            image_clip_size,
            sequence_id,
            image_id,
            output_images_path,
            cube_sides,
        )
        # Rename files
        clean_files(image_folder_path, image_id)
        new_feature = feature
    except requests.exceptions.HTTPError as err:
        print(err)
    except OSError as err:
        print(err)
    except KeyError as err:
        print(err)

    return new_feature


def clean_files(image_folder_path, image_id):
    """Remove files that was uploaded to s3, in order to optimize the fargate disk

    Args:
        image_folder_path (str): Location of the folder
        image_id (str): Id of the image
    """
    chumk_image_path = f"{image_folder_path}/{image_id}"
    for file in glob.glob(f"{chumk_image_path}/*.jpg"):
        side = Path(file).stem
        os.rename(
            f"{chumk_image_path}/{side}.jpg",
            f"{image_folder_path}/{image_id}_{side}.jpg",
        )


def process_image(features, output_images_path, image_clip_size, cube_sides):
    """Function to run in parallel mode to process mapillary images

    Args:
        features (fc): List of features objects
        output_images_path (str): Location to save clipped images
        image_clip_size (int): Size of the clipped image
        cube_sides (str): Sides of the image to clip

    Returns:
        fc: List of points that images were processed
    """
    # Process in parallel
    results = Parallel(n_jobs=-1)(
        delayed(download_clip_img)(
            feature, output_images_path, image_clip_size, cube_sides
        )
        for feature in tqdm(
            features, desc="Processing images for...", total=len(features)
        )
    )
    return results
