"""cvat.xml2csv: Skeleton of a function."""

import csv

from lxml import etree
from smart_open import open


def image_name(image):
    """Split image name."""
    return image.attrib["name"].split("/")


def to_csv(xml_file, csv_file):
    """An Awesome doc."""
    with open(xml_file, encoding="utf8") as file:
        tree = etree.parse(file)
    images = tree.findall(".//image")
    with open(csv_file, "w", encoding="UTF8", newline="") as f:
        data = [
            [
                image.attrib["id"],
                image.attrib["width"],
                image.attrib["height"],
                "/".join(image_name(image)[:-1]),
                image_name(image)[len(image_name(image)) - 1],
            ]
            for image in images
        ]

        writer = csv.writer(f)
        writer.writerow(["id", "width", "height", "path", "image"])
        writer.writerows(data)


def to_csv_full(in_file, csv_file):
    """An Awesome doc."""
    with open(in_file, encoding="utf8") as file:
        tree = etree.parse(file)

    images = tree.findall(".//image")
    objs = []
    for image in images:
        image_name = image.attrib["name"].split("/")
        boxes = image.findall(".//box")
        for box in boxes:
            attributes = box.findall(".//attribute")
            obj = {
                "img_id": image.attrib["id"],
                "img_width": image.attrib["width"],
                "img_height": image.attrib["height"],
                "img_path": "/".join(image_name[:-1]),
                "img_name": image_name[len(image_name) - 1],
                "box_label": box.attrib["label"],
                "box_occluded": box.attrib["occluded"],
                "box_xtl": box.attrib["xtl"],
                "box_ytl": box.attrib["ytl"],
                "box_xbr": box.attrib["xbr"],
                "box_ybr": box.attrib["ybr"],
            }
            for attr in attributes:
                obj["box_attr_" + attr.attrib["name"]] = attr.text
            objs.append(obj)
    with open(csv_file, "w", encoding="UTF8", newline="") as f:
        header = objs[0].keys()
        data = [list(row.values()) for row in objs]

        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
