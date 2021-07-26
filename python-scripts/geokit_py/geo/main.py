"""
Script for geo module
Author: @developmentseed
"""

import click


@click.group(chain=True)
def cli():
    """An Awesome doc."""
    # click.echo(click.style("========= GEO =============", fg="green"))
    pass


@cli.command("generate_id")
@click.option(
    "--in_file",
    required=True,
    help="Path to geojson file to be processed.",
)
@click.option("--id_label", "-l", default="id", help="key for id")
@click.option("--id_start", "-s", default=1, help="value to start id")
@click.option("--zeros", "-z", default=0, help="adds zeros at the beginning of the id")
@click.option(
    "--variation",
    "-v",
    default="NUMBER",
    type=click.Choice(["NUMBER", "UUID"], case_sensitive=False),
    help="type of id (number or uuid)",
)
@click.option(
    "--output_file", "-o", required=True, type=str, help="Path to geojson output file"
)
def run_generate_id(in_file, id_label, id_start, zeros, variation, output_file):
    """
    Addig a key <id_label> in the PROPERTIES in a geojson file, the value of id can start in 1 or start_count.

    """
    from .generateid import generateid

    generateid(in_file, id_label, id_start, zeros, variation, output_file)


@cli.command("osm2new")
@click.option(
    "--input_osm", required=True, type=str, help="Path to osm file to be processed."
)
@click.option("--output_osm", required=True, type=str, help="Path to osm output.")
def run_osm2new(input_osm, output_osm):
    """
    Removes some attributes of each feature such as: user, version, timestamp, changeset and uid.
    So it returns a new OSM file without these attributes.
    """
    from .osm2new import osm2new

    osm2new(input_osm, output_osm)


@cli.command("removeactionosm")
@click.option(
    "--input_osm", required=True, type=str, help="Path to osm file to be processed."
)
@click.option("--output_osm", required=True, type=str, help="Path to osm output.")
def run_removeactionosm(input_osm, output_osm):
    """
    Removes the objects with action=delete in a osm file.
    """
    from .remove_acction_obj import remove_action_obj

    remove_action_obj(input_osm, output_osm)


if __name__ == "__main__":
    cli()
