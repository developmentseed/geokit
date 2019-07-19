import sys
import string
import uuid
from lxml import etree

def ordinal(n):
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")

filename = sys.argv[1] if (len(sys.argv) > 1) else sys.exit("Invalid file name")
tree = etree.parse(filename)
tags = tree.findall(".//tag[@k='Id']")

for tag in tags:
    new_id = str(uuid.uuid4().fields[-1])[:8]
    old_id = tag.get('v')
    tag.set("v", new_id)
    print(old_id, new_id)

xml = "<?xml version='1.0' encoding='UTF-8'?>\n"+etree.tostring(tree, encoding='utf8')
new_file = open(sys.argv[1], 'w')
new_file.write(xml)
