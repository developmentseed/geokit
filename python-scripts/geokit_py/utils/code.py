"""utils.code: Skeleton of a function."""

import glob
import logging
from xml.etree import ElementTree as ET

import boto3
import click
from shapely.geometry import Polygon
from smart_open import open


def get_segments_root(root, v=False):
    """
    return segments from root obj.
    """
    try:
        segments = []
        for i in root.iter("segment"):
            o = {}
            for j in i:
                o[f"{j.tag}"] = j.text
            segments.append(o)
        if v:
            click.echo(
                click.style("--- segments created :) ", fg="bright_cyan", bold=True)
            )
        return segments
    except Exception as e:
        logging.error(e.__str__())


def read_xml(in_file, v=False):
    """
    Open xml file and return root  iterate file.
    """

    try:
        with open(in_file, encoding="utf8") as file:
            tree = ET.parse(file)
        if v:
            click.echo(click.style("--- xml readed :) ", fg="bright_cyan", bold=True))
        return tree.getroot()
    except Exception as e:
        logging.error(e.__str__())


def make_polygon(data):
    """
    Return a polygon from dataframe.
    """
    try:
        data = data[1]
        # rigth
        bounds = [
            (data["xtl"], data["ytl"]),
            (data["xbr"], data["ytl"]),
            (data["xtl"], data["ybr"]),
            (data["xtl"], data["ybr"]),
        ]
        poly = Polygon(bounds)
        return poly
    except Exception as e:
        logging.error(e.__str__())


def get_list_files_folder(folder_path, recursive, prefix):
    """return files from folder"""
    if not folder_path:
        return []
    if "s3://" in folder_path:
        bucket = folder_path.replace("s3://", "").split("/")[0]
        folder = f'{"/".join([i for i in folder_path.replace("s3://", "").split("/")[1:] if i])}/'.replace(
            "//", "/"
        )
        s3 = boto3.resource("s3")
        s3_bucket = s3.Bucket(bucket)
        if recursive:
            files_in_s3 = [
                f.key
                for f in s3_bucket.objects.filter(Prefix=folder).all()
                if prefix in f.key
            ]
        else:
            files_in_s3 = [
                f.key
                for f in s3_bucket.objects.filter(Prefix=folder).all()
                if prefix in f.key and "/" not in f.key.replace(folder, "")
            ]

        return [f"s3://{bucket}/{file}" for file in files_in_s3]
    # local folder
    folder_path = "/".join([i for i in folder_path.split("/") if i])
    if recursive:
        list(glob.glob(f"{folder_path}/**/*{prefix}"))
    return list(glob.glob(f"{folder_path}/*{prefix}"))
