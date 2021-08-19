"""
Script for cvat module
Author: @developmentseed
"""

import click


@click.group(chain=True)
def cli():
    """An Awesome doc."""
    # click.echo(click.style("========= CVAT =============", fg="green"))
    pass


@cli.command("intersectionbox")
@click.option(
    "--in_file", required=True, type=str, help="Path to xml cvat file to be processed."
)
@click.option(
    "--tolerance",
    default=70.0,
    type=float,
    required=False,
    help="tolerance to filter box area, default 70 (70% area of image, max area is 100%).",
)
def run_intersectionbox(in_file, tolerance):
    """
    find the boxes that intersect and are greater than the tolerance,
     for default tolerance is 70 (70% of the area of the small intersection box)
    """
    from .intersectionbox import intersectionbox

    intersectionbox(in_file, tolerance)


@cli.command("smallbox")
@click.option(
    "--in_file", required=True, type=str, help="Path to xml cvat file to be processed."
)
@click.option(
    "--tolerance",
    default=1.0,
    type=float,
    required=False,
    help="tolerance to filter box area, default 1 (1% image).",
)
def run_smallbox(in_file, tolerance):
    """
    find the boxes with an area smaller than the image, for default tolerance is 1 (1% of area image).
    """
    from .smallbox import smallbox

    smallbox(in_file, tolerance)


@cli.command("count_tag")
@click.option(
    "--xml_file",
    required=True,
    multiple=True,
    type=str,
    help="Path to xml cvat file to be processed.",
)
def run_count_tag(xml_file):
    """
    Count xml-cvat tags, acep multiple xml_file
    """
    from .count_tags import count_xml_tags

    stats = {}
    num_images = 0

    for i in list(xml_file):
        num = count_xml_tags(i, stats)
        num_images += num

    print(f"Total Images: {num_images}")
    for key in stats.keys():
        print(f"{key},\t {stats[key]}")


@cli.command("xml2csv")
@click.option(
    "--xml_file", required=True, type=str, help="Path to xml cvat file to be processed."
)
@click.option("--csv_file", required=True, type=str, help="Path to csv file  output.")
@click.option("--full", default=False, type=bool, help="full mode")
def run_xml2csv(xml_file, csv_file, full):
    """
    Convert xml to csv file
    """
    from .xml2csv import to_csv, to_csv_full

    if full:
        to_csv_full(xml_file, csv_file)
    else:
        to_csv(xml_file, csv_file)


@cli.command("npz2xml")
@click.option("--npz_file", required=True, type=str, help="labelMaker npz file")
@click.option("--img_path", required=True, type=str, help="path of the images in CVAT")
@click.option("--img_label", required=True, type=str, help="label image eg : tower.")
def run_npz2xml(npz_file, img_path, img_label):
    """
    NPZ file to XML cvat imput format
    """
    from .npz2xml import npz2xml

    npz2xml(npz_file, img_path, img_label)


@cli.command("xml2npz")
@click.option("--xml_file", required=True, type=str, help="cvat xml dump file")
@click.option("--npz_file", required=True, type=str, help="npz file")
def run_xml2npz(xml_file, npz_file):
    """
    NPZ file to XML cvat imput format
    """
    import numpy as np
    from .xml2npz import getTiles

    tiles = getTiles(xml_file)
    np.savez(npz_file, **tiles)


@cli.command("downsized_imgs")
@click.option("--img_path", required=True, type=str, help="Image folder")
@click.option("--output_path", required=True, type=str, help="Image output folder")
def run_downsized_imgs(img_path, output_path):
    """
    Add all the images that you want to downsize in a folder, supports jpg files and the files will be resized to 512X512.
    """
    from .downsized_imgs import downsized_imgs

    downsized_imgs(img_path, output_path)


@cli.command("fix_ordinal_suffixes")
@click.option(
    "--xml_input",
    required=True,
    type=str,
    help="Path to xml cvat file to be processed.",
)
@click.option("--xml_output", required=True, type=str, help="Path to xml cvat output.")
def run_fix_ordinal_suffixes(xml_input, xml_output):
    """An Awesome doc."""
    from .fix_ordinal_suffixes import fix_ordinal_suffixes

    fix_ordinal_suffixes(xml_input, xml_output)


if __name__ == "__main__":
    cli()
