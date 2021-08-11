"""geo.osm2new: Skeleton of a function."""

from lxml import etree
from tqdm import tqdm

attribs = ["user", "version", "timestamp", "changeset", "uid"]


def osm2new(input_osm, output_osm):
    """An Awesome doc."""
    tree = etree.parse(input_osm)
    nodes = tree.findall(".//node")
    ways = tree.findall(".//way")
    relations = tree.findall(".//relation")
    dict = {}
    index = -5000
    for node in tqdm(nodes, desc=f"Process nodes"):
        index = index - 1
        dict[node.attrib["id"]] = index
        node.attrib["id"] = str(index)
        node.attrib["action"] = "modify"
        for at in attribs:
            if at in node.attrib:
                del node.attrib[at]

    for way in tqdm(ways, desc=f"Process ways"):
        index = index - 1
        dict[way.attrib["id"]] = index
        way.attrib["id"] = str(index)
        way.attrib["action"] = "modify"
        for at in attribs:
            if at in way.attrib:
                del way.attrib[at]
        nds = way.findall(".//nd")
        for nd in nds:
            if nd.attrib["ref"] in dict:
                nd.attrib["ref"] = str(dict[nd.attrib["ref"]])

    for relation in tqdm(relations, desc=f"Process relations"):
        index = index - 1
        dict[relation.attrib["id"]] = index
        relation.attrib["id"] = str(index)
        relation.attrib["action"] = "modify"
        for at in attribs:
            if at in relation.attrib:
                del relation.attrib[at]

        members = relation.findall(".//member")
        for member in members:
            if member.attrib["ref"] in dict:
                member.attrib["ref"] = str(dict[member.attrib["ref"]])

    xml = b"<?xml version='1.0' encoding='UTF-8'?>\n" + etree.tostring(tree, pretty_print=True, encoding="utf8")
    new_file = open(output_osm, "w")
    new_file.write(xml.decode("utf8"))
