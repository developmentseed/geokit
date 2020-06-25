# encoding=utf8
# !/usr/bin/python
import string
from lxml import etree
import sys

# reload
try:
    reload(sys)
    sys.setdefaultencoding('utf8')

except NameError:
    # Python 3
    try:
        from importlib import reload
    except ImportError:
        from imp import reload

    reload(sys)

stats = {}
num_images = 0
num_images_with_box = 0


def count(file):
    tree = etree.parse(file)
    images = tree.findall(".//image")
    boxes = tree.findall(".//box")
    num_images_int = len(images)
    num_images_w_box_int = 0
    for box in boxes:
        # Count for buildings
        attributes = box.findall(".//attribute")
        for attr in attributes:
            if stats.get(attr.attrib['name']):
                if stats[attr.attrib['name']].get(attr.text):
                    stats[attr.attrib['name']][attr.text] = stats[attr.attrib['name']][attr.text] + 1
                else:
                    stats[attr.attrib['name']][attr.text] = 1
            else:
                stats[attr.attrib['name']] = {}
                stats[attr.attrib['name']][attr.text] = 1
        if stats.get(box.attrib['label']):
            stats[box.attrib['label']] = stats[box.attrib['label']] + 1
        else:
            stats[box.attrib['label']] = 1
    for image in images:
        if image.findall(".//box"):
            num_images_w_box_int += 1
    return num_images_int, num_images_w_box_int


for i in range(1, len(sys.argv)):
    num_images_i, num_images_wbox = count(sys.argv[i])
    num_images += num_images_i
    num_images_with_box += num_images_wbox

for key in stats.keys():
    print("%s,%s" % (key, stats[key]))

print("Total Images: %s" % (num_images))
print("Total Images with box: %s" % (num_images_with_box))
