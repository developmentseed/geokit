#!/usr/bin/env python
from xml.etree import ElementTree as ET
import logging
import csv
import click


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


def save_csv(ouput_file_name, data, ouput_path='./ouput', v=False):
    """
    save csv file
    ouput is path to ouput file
    """
    try:
        ouput_file_name_path = f'{ouput_path}/{ouput_file_name}'

        with open(ouput_file_name_path, 'w', newline='') as f:
            f.truncate()
            writer = csv.writer(f)
            writer.writerows(data)
            if v:
                click.echo(click.style('--- csv saved :) ', fg='bright_cyan', bold=True))
    except Exception as e:
        logging.error(e.__str__())


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
