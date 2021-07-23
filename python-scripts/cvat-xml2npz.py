# encoding=utf8
#!/usr/bin/python
import numpy as np
from lxml import etree
from os import path
import sys

def getTiles(file):
    tree = etree.parse(file)
    images = tree.findall(".//image")
    tiles = {}
    for image in images:
        tile = path.splitext(path.basename(image.attrib['name']))[0]
        boxes = image.findall(".//box")
        boxesList = []
        for box in boxes:
            boxesList.append([
                float(box.attrib['xtl']),
                float(box.attrib['ytl']),
                float(box.attrib['xbr']),
                float(box.attrib['ybr']),
                int(1)])
        tiles[tile] = boxesList
    return tiles

tiles = getTiles(sys.argv[1])
outputFile = path.splitext(sys.argv[1])[0] + ".npz"
np.savez(outputFile, **tiles)
