"""utils.code: Skeleton of a function."""

import logging
from xml.etree import ElementTree as ET

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
