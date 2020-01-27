# encoding=utf8
#!/usr/bin/python
import sys
import string
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')
for i in range(1, len(sys.argv)):
    file = sys.argv[i] if (len(sys.argv) > 1) else sys.exit("Invalid file name left")
    tree = etree.parse(file)
    images = tree.findall(".//image")
    num_imagesPRE = len(images)
    boxes = tree.findall(".//box")
    print("id,width,height,path,image")
    for image in images:
        imageName=image.attrib['name'].split("/")
        print("%s,%s,%s,%s,%s"% (image.attrib['id'],image.attrib['width'],image.attrib['height'],'/'.join(imageName[:-1]),imageName[len(imageName)-1]))