from lxml import etree


def remove_action_obj(input_osm, output_osm):
    tree = etree.parse(input_osm)
    nodes = tree.findall(".//node")
    ways = tree.findall(".//way")
    relations = tree.findall(".//relation")
    action = "delete"
    for node in nodes:
        if "action" in node.attrib and node.attrib["action"] == action:
            node.getparent().remove(node)
    for way in ways:
        if "action" in way.attrib and way.attrib["action"] == action:
            way.getparent().remove(way)
    for relation in relations:
        if "action" in relation.attrib and relation.attrib["action"] == action:
            relation.getparent().remove(relation)
    xml = "<?xml version='1.0' encoding='UTF-8'?>\n" + etree.tostring(
        tree, encoding="utf8"
    )
    new_file = open(output_osm, "w")
    new_file.write(xml)
