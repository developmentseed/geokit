from xml.etree import ElementTree as ET
from shapely.geometry import Polygon
import click
import logging


def get_segments_root(root, v=False):
    """
      return segments from root obj
      """
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
    """
       return a polygon from dataframe
    """
    try:
        data = data[1]
        # rigth
        bounds = [(data['xtl'], data['ytl']), (data['xbr'], data['ytl']), (data['xtl'], data['ybr']),
                  (data['xtl'], data['ybr'])]
        poly = Polygon(bounds)
        return poly
    except Exception as e:
        logging.error(e.__str__())
