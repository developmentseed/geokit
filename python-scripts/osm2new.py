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
  del node.attrib["user"]
  del node.attrib["version"]
  del node.attrib["timestamp"]
  del node.attrib["changeset"]
  del node.attrib["uid"]
for way in ways:
  index=index-1
  dict[way.attrib['id']]=index
  way.attrib['id']=str(index)
  way.attrib['action']='modify'
  del way.attrib["user"]
  del way.attrib["version"]
  del way.attrib["timestamp"]
  del way.attrib["changeset"]
  del way.attrib["uid"]
  nds=way.findall(".//nd")
  for nd in nds:
    nd.attrib['ref'] = str(dict[nd.attrib['ref']])
for relation in relations:
  index=index-1
  dict[relation.attrib['id']]=index
  relation.attrib['id']=str(index)
  relation.attrib['action']='modify'
  del relation.attrib["user"]
  del relation.attrib["version"]
  del relation.attrib["timestamp"]
  del relation.attrib["changeset"]
  del relation.attrib["uid"]
  members=relation.findall(".//member")
  for member in members:
    if member.attrib['ref'] in dict:
      member.attrib['ref'] = str(dict[member.attrib['ref']])
xml = "<?xml version='1.0' encoding='UTF-8'?>\n"+etree.tostring(tree, encoding='utf8')
new_file = open(osmfilename[:-4]+'_new'+osmfilename[-4:], 'w')
new_file.write(xml)