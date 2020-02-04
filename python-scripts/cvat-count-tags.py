# encoding=utf8
#!/usr/bin/python
import sys
import string
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')

stats={}
num_images=0

def count(file):
    tree = etree.parse(file)
    images = tree.findall(".//image")
    boxes = tree.findall(".//box")
    for box in boxes:
        # Count for buildings
        attributes=box.findall(".//attribute")
        for attr in attributes:
            if stats.get(attr.attrib['name']):
                if stats[attr.attrib['name']].get(attr.text):
                    stats[attr.attrib['name']][attr.text]=stats[attr.attrib['name']][attr.text]+1
                else:
                    stats[attr.attrib['name']][attr.text]=1
            else:
                stats[attr.attrib['name']]={}
                stats[attr.attrib['name']][attr.text]=1
        if stats.get(box.attrib['label']):
            stats[box.attrib['label']]=stats[box.attrib['label']]+1
        else:
            stats[box.attrib['label']]=1
    return len(images)

for i in range(1, len(sys.argv)):
    num = count(sys.argv[i])
    num_images=num_images+num


print("Total Images:%s" %(num_images))
for key in stats.keys():
        print("%s,%s"%(key,stats[key]))