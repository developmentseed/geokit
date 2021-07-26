"""cvat.intersectionbox: Skeleton of a function."""

import itertools
import logging

import pandas as pd
from geokit_py.utils.code import get_segments_root, make_polygon, read_xml


def tree2list(root):
    """An Awesome doc."""
    segments = get_segments_root(root)
    list_image_data = []
    list_image_data_columns = (
        "url",
        "id-image",
        "width",
        "height",
        "xtl",
        "xbr",
        "ytl",
        "ybr",
        "x",
        "y",
        "area",
    )

    try:
        for i in root:
            if i.tag == "image":
                url = ""
                image_id = int(i.get("id"))
                for j in segments:
                    if int(j.get("start")) <= image_id <= int(j.get("stop")):
                        url = j.get("url")
                area_imagen = float(
                    float(i.get("width")) * float(i.get("height"))
                ).__round__(3)

                for j in i:
                    if j.tag == "box":
                        image = [
                            f'{url}&frame={i.get("id")}',
                            int(i.get("id")),
                            float(i.get("width")),
                            float(i.get("height")),
                            float(j.get("xtl")),
                            float(j.get("xbr")),
                            float(j.get("ytl")),
                            float(j.get("ybr")),
                        ]

                        x = abs(float(j.get("xbr")) - float(j.get("xtl")))
                        y = abs(float(j.get("ybr")) - float(j.get("ytl")))
                        a_box = float(x * y).__round__(3)
                        image.append(x)
                        image.append(y)
                        image.append(a_box)
                        list_image_data.append(image)

    except Exception as e:
        logging.error(e.__str__())
    else:
        return pd.DataFrame(list_image_data, columns=list_image_data_columns)


def intersectionbox(in_file, toleranci):
    """
    Processes the area of cvt file and filter small boxes.
    """
    if 0.0 <= toleranci >= 100.0:
        return logging.error("The toleranci has error ")

    toleranci = toleranci / 100

    list_image_err = [
        ("url", "id_image", "area intersection %"),
    ]

    root = read_xml(in_file)
    df = tree2list(root)
    try:
        if not df.empty:
            for i, k in df.groupby("url"):
                is_report = False
                err_rep = 0
                id_image = ""

                if k.__len__() > 1:
                    list_polygon_box = []
                    for j in k.iterrows():
                        id_image = j[1]["id-image"]
                        list_polygon_box.append(make_polygon(j))
                    for j in itertools.combinations(list_polygon_box, 2):
                        interseccion = j[0].intersection(j[1])
                        if interseccion:
                            mayor, menor = j
                            if j[0].area <= j[1].area:
                                menor, mayor = j
                            if (
                                float(interseccion.area / menor.area) >= toleranci
                                and not is_report
                            ):
                                err_rep = float(
                                    interseccion.area / menor.area
                                ).__round__(4)
                                is_report = True
                if is_report:
                    list_image_err.append((i, id_image, err_rep))

    except Exception as e:
        logging.error(e.__str__())
    else:
        for i in list_image_err:
            print(",".join(map(str, i)))
