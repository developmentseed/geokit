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
dict = {}
index = -5000
for node in nodes:
  index=index-1
  dict[node.attrib['id']]=index
  node.attrib['id']=str(index)
  node.attrib['action']='modify'
  if "user" in node.attrib: del node.attrib["user"]
  if "version" in node.attrib: del node.attrib["version"]
  if "timestamp" in node.attrib: del node.attrib["timestamp"]
  if "changeset" in node.attrib: del node.attrib["changeset"]
  if "uid" in node.attrib: del node.attrib["uid"]
for way in ways:
  index=index-1
  dict[way.attrib['id']]=index
  way.attrib['id']=str(index)
  way.attrib['action']='modify'
  if "user" in way.attrib: del way.attrib["user"]
  if "version" in way.attrib: del way.attrib["version"]
  if "timestamp" in way.attrib: del way.attrib["timestamp"]
  if "changeset" in way.attrib: del way.attrib["changeset"]
  if "uid" in way.attrib: del way.attrib["uid"]
  nds=way.findall(".//nd")
  for nd in nds:
    if nd.attrib['ref'] in dict:
      nd.attrib['ref'] = str(dict[nd.attrib['ref']])
for relation in relations:
  index=index-1
  dict[relation.attrib['id']]=index
  relation.attrib['id']=str(index)
  relation.attrib['action']='modify'
  if "user" in relation.attrib: del relation.attrib["user"]
  if "version" in relation.attrib: del relation.attrib["version"]
  if "timestamp" in relation.attrib: del relation.attrib["timestamp"]
  if "changeset" in relation.attrib: del relation.attrib["changeset"]
  if "uid" in relation.attrib: del relation.attrib["uid"]
  members=relation.findall(".//member")
  for member in members:
    if member.attrib['ref'] in dict:
      member.attrib['ref'] = str(dict[member.attrib['ref']])
xml = "<?xml version='1.0' encoding='UTF-8'?>\n"+etree.tostring(tree, encoding='utf8')
new_file = open(sys.argv[2], 'w')
new_file.write(xml)