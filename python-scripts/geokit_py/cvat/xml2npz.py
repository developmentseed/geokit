"""cvat.xml2npz: Skeleton of a function."""

from os import path

from lxml import etree


def getTiles(file):
    """An Awesome doc."""
    tree = etree.parse(file)
    images = tree.findall(".//image")
    tiles = {}
    for image in images:
        tile = path.splitext(path.basename(image.attrib["name"]))[0]
        boxes = image.findall(".//box")
        boxesList = []
        for box in boxes:
            boxesList.append(
                [
                    float(box.attrib["xtl"]),
                    float(box.attrib["ytl"]),
                    float(box.attrib["xbr"]),
                    float(box.attrib["ybr"]),
                    int(1),
                ]
            )
        tiles[tile] = boxesList
    return tiles
