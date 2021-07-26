import numpy as np
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom

def npz2xml(npzFile, imgFolder, imgLabel):
    root = ET.Element('annotations')
    version = ET.SubElement(root, 'version')
    version.text = str('1.1')
    # Read npz file
    labels = np.load(npzFile)
    index = 0
    for tile in labels.files:
        boxes = labels[tile]
        image = ET.SubElement(root, 'image')
        image.attrib['id'] = str(index)
        image.attrib['name'] = str(imgFolder + '/' + tile + '.png')
        image.attrib['width'] = str('256')
        image.attrib['height'] = str('256')
        for box in boxes:
            xmlBox = ET.SubElement(image, 'box')
            xmlBox.attrib['label'] = str(imgLabel)
            xmlBox.attrib['occluded'] = str('0')
            xmlBox.attrib['xtl'] = str(box[0])
            xmlBox.attrib['ytl'] = str(box[1])
            xmlBox.attrib['xbr'] = str(box[2])
            xmlBox.attrib['ybr'] = str(box[3])
        index = index+1
    # xml = ET.tostring(root, encoding='utf8').decode('utf8')
    # new_file = open(path.basename(xmlFile)+"-fixed.xml", 'w')
    # new_file.write(xml)
    print(prettify(root))

def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
