"""cvat.fix_ordinal_suffixes: Skeleton of a function."""

from lxml import etree
from smart_open import open


def ordinal(n):
    """ordinal."""
    if 10 <= n % 100 < 20:
        return str(n) + "th"
    else:
        return str(n) + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def fix_ordinal_suffixes(xml_input, xml_output):
    "Fix ordinal suffixes of xml file."
    with open(xml_input, encoding="utf8") as file:
        tree = etree.parse(file)
    addr_streets = tree.findall(".//tag[@k='addr:street']")

    for addr_street in addr_streets:
        old_name = addr_street.get("v").encode("utf-8").strip()
        new_name = addr_street.get("v").encode("utf-8").strip()
        num_bef = ""
        num_aft = ""
        for i, c in enumerate(new_name):
            if c.isdigit():
                start = i
                while i < len(new_name) and new_name[i].isdigit():
                    i += 1
                num_bef = new_name[start:i]
                if new_name[start + i : i + 1].isspace():
                    num_aft = ordinal(int(num_bef))
                    new_name = new_name.replace(num_bef, num_aft)

                if addr_street.get("v") != new_name:
                    addr_street.set("v", new_name)
                    parent = addr_street.getparent()
                    parent.attrib["action"] = "modify"
                break
        print(f"- {old_name} > {new_name}")
    xml_tree = (
        etree.tostring(tree, encoding="utf8", pretty_print=True)
        .decode("utf8")
        .replace('"', "'")
    )
    with open(xml_output, "wb") as new_file:
        new_file.write(b"<?xml version='1.0' encoding='UTF-8'?>\n")
        new_file.write(bytes(xml_tree.encode("utf8")))
