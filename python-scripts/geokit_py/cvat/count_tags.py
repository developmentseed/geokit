"""cvat.count_tags: Skeleton of a function."""

from lxml import etree


def count_xml_tags(file, stats):
    """An Awesome doc."""

    tree = etree.parse(file)
    images = tree.findall(".//image")
    images_with_box = tree.xpath("//image[box]")

    boxes = tree.findall(".//box")
    for box in boxes:
        # attributes
        attributes = box.findall(".//attribute")
        for attr in attributes:
            name = str(attr.attrib["name"])
            text = str(attr.text)
            if not stats.get(name):
                stats[name] = {}
            if not stats[name].get(text):
                stats[name][text] = 0
            stats[name][text] += 1

        # bbox
        label = str(box.attrib["label"])
        if not stats.get(label):
            stats[label] = 0
        stats[label] += 1
    return len(images), len(images_with_box)
