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
@click.option("--id_label", default="id", help="key for id")
@click.option("--id_start", default=1, type=int, help="value to start id")
@click.option("--zeros", default=0, help="adds zeros at the beginning of the id")
@click.option(
    "--variation",
    default="NUMBER",
    type=click.Choice(["NUMBER", "UUID"], case_sensitive=False),
    help="type of id (number or uuid)",
)
@click.option(
    "--output_file", required=True, type=str, help="Path to geojson output file"
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


@cli.command("features_in_polygons")
@click.option(
    "--geojson_in_polygon", required=True, type=str, help="Path to geojson polygons."
)
@click.option(
    "--geojson_in_features", required=True, type=str, help="Path to geojson features."
)
@click.option(
    "--tags_polygon",
    required=False,
    type=str,
    default=[],
    multiple=True,
    help="fields geojson_in_polygon to add features.",
)
@click.option(
    "--mode_filter",
    required=True,
    default="include__centroid",
    type=click.Choice(
        [
            "include",
            "include__centroid",
        ],
        case_sensitive=True,
    ),
    help="mode of filter.",
)
@click.option(
    "--mode_output",
    required=True,
    default="normal",
    type=click.Choice(["normal", "where", "tags_polygon"], case_sensitive=True),
    help="mode of file output.",
)
@click.option(
    "--geojson_out_features",
    required=True,
    type=str,
    help="Path to geojson features output.",
)
def run_features_in_polygons(
    geojson_in_polygon,
    geojson_in_features,
    tags_polygon,
    mode_filter,
    mode_output,
    geojson_out_features,
):
    """
    Script to add tag '_where' and fields bby location (mode_filter).
    """
    from .features_in_polygons import features_in_polygons

    features_in_polygons(
        geojson_in_polygon,
        geojson_in_features,
        tags_polygon,
        mode_filter,
        mode_output,
        geojson_out_features,
    )

    if __name__ == "__main__":
        cli()
