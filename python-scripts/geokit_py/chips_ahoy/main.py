"""
Script for chips_ahoy module
Author: @developmentseed
"""

import click


@click.group(chain=True)
def cli():
    """An Awesome doc."""
    # click.echo(click.style("========= CHIPS AHOY =============", fg="green"))
    pass


@cli.command("fctile")
@click.option(
    "--geojson_file",
    help="Geojson file",
    required=True,
    type=str,
)
@click.option(
    "--zoom",
    help="Zoom to get the tile",
    required=True,
    type=int,
    default=18,
)
@click.option(
    "--url_map_service",
    help="Tile map service url",
    required=True,
    type=str,
    default="http://tile.openstreetmap.org/{z}/{x}/{y}.png",
)
@click.option(
    "--geojson_output",
    help="Original geojson with the attributes: tile, url",
    required=True,
    type=str,
)
@click.option(
    "--chuck",
    help="chuck size",
    type=int,
    required=False,
    default=0,
)
def run_fctile(geojson_file, zoom, url_map_service, geojson_output, chuck):
    """Script for add tile and url-tiles."""
    from .fctile import fctile

    fctile(geojson_file, zoom, url_map_service, geojson_output, chuck)


@cli.command("filter_chips")
@click.option(
    "--geojson_file",
    help="Geojson file",
    required=True,
    type=str,
)
@click.option(
    "--clean_fields",
    help="Clean chips-ahoy fields",
    required=False,
    default=False,
    is_flag=True,
)
@click.option(
    "--geojson_output",
    help="Geojson separate in no , yes (tile - point)",
    type=str,
    required=True,
)
def run_filter_chips(geojson_file, clean_fields, geojson_output):
    """Script separate schools in yes - no"""
    from .filter_chips import filter_chips

    filter_chips(geojson_file, clean_fields, geojson_output)


if __name__ == "__main__":
    cli()
