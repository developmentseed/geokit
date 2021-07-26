from lxml import etree


def count_xml_tags(file, stats):
    tree = etree.parse(file)
    images = tree.findall(".//image")
    boxes = tree.findall(".//box")
    for box in boxes:
        # Count for buildings
        attributes = box.findall(".//attribute")
        for attr in attributes:
            if stats.get(attr.attrib['name']):
                if stats[attr.attrib['name']].get(attr.text):
                    stats[attr.attrib['name']][attr.text] = stats[attr.attrib['name']][attr.text] + 1
                else:
                    stats[attr.attrib['name']][attr.text] = 1
            else:
                stats[attr.attrib['name']] = {}
                stats[attr.attrib['name']][attr.text] = 1
        if stats.get(box.attrib['label']):
            stats[box.attrib['label']] = stats[box.attrib['label']] + 1
        else:
            stats[box.attrib['label']] = 1
    return len(images)
