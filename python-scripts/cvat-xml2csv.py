# encoding=utf8
#!/usr/bin/python
import sys
import string
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def toCSV(file):
    tree = etree.parse(file)
    images = tree.findall(".//image")
    num_imagesPRE = len(images)
    boxes = tree.findall(".//box")
    print("id,width,height,path,image")
    for image in images:
        imageName = image.attrib['name'].split("/")
        print("%s,%s,%s,%s,%s" % (image.attrib['id'], image.attrib['width'],
                                  image.attrib['height'], '/'.join(imageName[:-1]), imageName[len(imageName)-1]))

def toCSVFull(file):
    tree = etree.parse(file)
    images = tree.findall(".//image")
    objs = []
    for image in images:
        imageName = image.attrib['name'].split("/")
        boxes = image.findall(".//box")
        for box in boxes:
            attributes = box.findall(".//attribute")
            obj = {
                "img_id": image.attrib['id'],
                "img_width": image.attrib['width'],
                "img_height": image.attrib['height'],
                "img_path": '/'.join(imageName[:-1]),
                "img_name": imageName[len(imageName)-1],
                "box_label": box.attrib['label'],
                "box_occluded": box.attrib['occluded'],
                "box_xtl": box.attrib['xtl'],
                "box_ytl": box.attrib['ytl'],
                "box_xbr": box.attrib['xbr'],
                "box_ybr": box.attrib['ybr']
            }
            for attr in attributes:
                obj["box_attr_" + attr.attrib['name']] = attr.text
            objs.append(obj)
    print(','.join(objs[0].keys()))
    for row in objs:
        print(','.join(row.values()))

if sys.argv[1] == "--full":
    toCSVFull(sys.argv[2])
else:
    toCSV(sys.argv[1])
