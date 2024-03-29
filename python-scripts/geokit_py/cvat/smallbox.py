"""cvat.smallbox: Skeleton of a function."""

import logging

from geokit_py.utils.code import get_segments_root, read_xml


def smallbox(in_file, tolerance):
    """
    Processes the area of cvt file and filter small boxes.
    """
    # vars
    # function_name = 'SMALLBOX'
    # path = os.path.dirname(in_file)
    # file_name = os.path.basename(in_file)
    tolerance = tolerance / 100
    # ouput_file_name = f'{file_name.lower().replace(".xml", "")}_{function_name}_OUTPUT.csv'
    list_image_err = [
        [
            "url",
            "id-image",
            "area",
        ]
    ]

    root = read_xml(in_file)

    segments = get_segments_root(root)

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
                        image = [f'{url}&frame={i.get("id")}', int(i.get("id"))]
                        x = abs(float(j.get("xbr")) - float(j.get("xtl")))
                        y = abs(float(j.get("ybr")) - float(j.get("ytl")))
                        a_box = float(x * y).__round__(3)
                        image.append(a_box)

                        if (a_box / area_imagen) <= tolerance:
                            list_image_err.append(image)

    except Exception as e:
        logging.error(e.__str__())
    else:
        # save_csv(ouput_file_name, list_image_err,ouput_path)
        # df = DataFrame(list_image_err)
        # print version
        for i in list_image_err:
            print(",".join(map(str, i)))
