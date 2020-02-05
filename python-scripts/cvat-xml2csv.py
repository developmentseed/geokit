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
                "id": image.attrib['id'],
                "width": image.attrib['width'],
                "height": image.attrib['height'],
                "path": '/'.join(imageName[:-1]),
                "image": imageName[len(imageName)-1]
            }
            for attr in attributes:
                obj[attr.attrib['name']] = attr.text
            objs.append(obj)

    print(','.join(objs[0].keys()))
    for row in objs:
        print(','.join(row.values()))

print(sys.argv)
if(len(sys.argv)>2 and sys.argv[1] == '-f'):
    toCSVFull(sys.argv[2])
else:
    toCSV(sys.argv[1])
