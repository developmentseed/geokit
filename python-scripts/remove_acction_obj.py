# encoding=utf8
#!/usr/bin/python
import sys
import string
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')
osmfilename = sys.argv[1] if (len(sys.argv) > 1) else sys.exit("Invalid file name")
tree = etree.parse(osmfilename)
nodes = tree.findall(".//node")
ways = tree.findall(".//way")
relations = tree.findall(".//relation")
action = 'delete'
for node in nodes:
  if 'action' in node.attrib and node.attrib['action'] == action:
    node.getparent().remove(node)
for way in ways:
  if 'action' in way.attrib and way.attrib['action'] == action:
    way.getparent().remove(way)
for relation in relations:
  if 'action' in relation.attrib and relation.attrib['action'] == action:
    relation.getparent().remove(relation)
xml = "<?xml version='1.0' encoding='UTF-8'?>\n"+etree.tostring(tree, encoding='utf8')
new_file = open(sys.argv[2], 'w')
new_file.write(xml)