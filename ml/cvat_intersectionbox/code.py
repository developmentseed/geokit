from xml.etree import ElementTree as ET
import pandas as pd
import logging
import click
from shapely.geometry import Polygon
import itertools


def get_segments_root(root, v=False):
    try:
        segments = []
        for i in root.iter('segment'):
            o = {}
            for j in i:
                o[f'{j.tag}'] = j.text
            segments.append(o)
        if v:
            click.echo(click.style('--- segments created :) ', fg='bright_cyan', bold=True))
        return segments
    except Exception as e:
        logging.error(e.__str__())


def read_xml(in_file, v=False):
    """
    open xml file and return root  iterate file
    """

    try:
        tree = ET.parse(in_file)
        if v:
            click.echo(click.style('--- xml readed :) ', fg='bright_cyan', bold=True))
        return tree.getroot()
    except Exception as e:
        logging.error(e.__str__())


def make_polygon(data):
    try:
        data = data[1]
        # rigth
        bounds = [(data['xtl'], data['ytl']), (data['xbr'], data['ytl']), (data['xtl'], data['ybr']),
                  (data['xtl'], data['ybr'])]
        poly = Polygon(bounds)
        return poly
    except Exception as e:
        logging.error(e.__str__())


def et2list(root):
    segments = get_segments_root(root)
    list_image_data = []
    list_image_data_columns = ('url', 'id-image', 'width', 'height', 'xtl', 'xbr', 'ytl', 'ybr', 'x', 'y', 'area')

    try:
        for i in root:
            if i.tag == 'image':
                url = ''
                image_id = int(i.get('id'))
                for j in segments:
                    if int(j.get('start')) <= image_id <= int(j.get('stop')):
                        url = j.get('url')
                area_imagen = float(float(i.get('width')) * float(i.get('height'))).__round__(3)

                for j in i:
                    if j.tag == 'box':
                        image = [f'{url}&frame={i.get("id")}', int(i.get('id')), float(i.get('width')),
                                 float(i.get('height')), float(j.get('xtl')), float(j.get('xbr')),
                                 float(j.get('ytl')), float(j.get('ybr'))]

                        x = abs(float(j.get('xbr')) - float(j.get('xtl')))
                        y = abs(float(j.get('ybr')) - float(j.get('ytl')))
                        a_box = float(x * y).__round__(3)
                        image.append(x)
                        image.append(y)
                        image.append(a_box)
                        list_image_data.append(image)

    except Exception as e:
        logging.error(e.__str__())
    else:
        return pd.DataFrame(list_image_data, columns=list_image_data_columns)


@click.command()
@click.option("--in", "-i", "in_file", required=True, help="Path to xml cvt file to be processed.", )
@click.option("--toleranci", "-t", default=70.0,
              help="toleranci to filter box area, default 70 (70% area of image, max area is 100%).")
def process(in_file, toleranci):
    """
    Processes the area of cvt file and filter small boxes
    """
    if 0.0 <= toleranci >= 100.0:
        return logging.error('The toleranci has error ')

    toleranci = toleranci / 100

    list_image_err = [('url', 'area intersection %'), ]

    root = read_xml(in_file)
    df = et2list(root)
    try:
        if not df.empty:
            for i, k in df.groupby('url'):
                is_report = False
                err_rep = 0
                if k.__len__() > 1:
                    list_polygon_box = []
                    for j in k.iterrows():
                        list_polygon_box.append(make_polygon(j))
                    for j in itertools.combinations(list_polygon_box, 2):
                        interseccion = j[0].intersection(j[1])
                        if interseccion:
                            mayor, menor = j
                            if j[0].area <= j[1].area:
                                menor, mayor = j
                            if float(interseccion.area / menor.area) >= toleranci and not is_report:
                                err_rep = float(interseccion.area / menor.area).__round__(4)
                                is_report = True
                if is_report:
                    list_image_err.append((i, err_rep))


    except Exception as e:
        logging.error(e.__str__())
    else:
        for i in list_image_err:
            print(f'{i[0]},{i[1]}')


if __name__ == '__main__':
    process()
