import sys
import string
import uuid
from lxml import etree

filename = sys.argv[1] if (len(sys.argv) > 1) else sys.exit("Invalid file name")
tree = etree.parse(filename)
ways = tree.findall(".//way")
relations = tree.findall(".//relation")
index=0
for way in ways:
    new_id = str(index) + '_' + str(uuid.uuid4().fields[-1])[:8]
    neewTag = etree.SubElement(way, "tag")
    neewTag.attrib['k']="idBuilding"
    neewTag.attrib['v']=new_id
    index = index + 1
    way.attrib['action']='modify'

for relation in relations:
    new_id = str(index) + '_' + str(uuid.uuid4().fields[-1])[:8]
    neewTag = etree.SubElement(relation, "tag")
    neewTag.attrib['k']="idBuilding"
    neewTag.attrib['v']=new_id
    index = index + 1
    relation.attrib['action']='modify'

xml = "<?xml version='1.0' encoding='UTF-8'?>\n"+etree.tostring(tree, encoding='utf8')
new_file = open(sys.argv[2], 'w')
new_file.write(xml)