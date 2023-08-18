"""
Script for mapillary module
Author: @developmentseed
"""

import click

from geokit_py.utils.map_utils import validate_geojson_file


@click.group(chain=True)
def cli():
    """An Awesome doc."""
    # click.echo(click.style("========= MAPILLARY =============", fg="green"))
    pass


# =========================================
# ========== GET MAPILLARY POINTS =========
# =========================================


@cli.command("get_mapillary_points")
@click.option(
    "--bbox",
    default="-83.2263319287,42.3489816308,-83.2230326577,42.3507715447",
    required=False,
    help="bbox",
)
@click.option(
    "--geojson_boundaries",
    default="",
    required=False,
    help="geojson_boundaries",
)
@click.option(
    "--field_name",
    default="",
    required=False,
    help="a field name from geojson boundaries",
)
@click.option(
    "--timestamp_from",
    default=0,
    type=int,
    required=False,
    help="timestamp_from value in milliseconds",
)
@click.option(
    "--only_pano",
    default=False,
    type=bool,
    required=False,
    is_flag=True,
    help="get only pano images",
)
@click.option(
    "--organization_ids",
    default="",
    type=str,
    required=False,
    help="organization id filter",
)
@click.option(
    "--output_file_point",
    default="data/points.geojson",
    type=click.Path(),
    help="Pathfile for geojson point file",
)
@click.option(
    "--output_file_sequence",
    default="data/sequences.geojson",
    type=click.Path(),
    help="Pathfile for geojson sequence file",
)
def run_get_mapillary_points(
    bbox,
    geojson_boundaries,
    field_name,
    timestamp_from,
    only_pano,
    organization_ids,
    output_file_point,
    output_file_sequence,
):
    """
    Script to get points and sequence for a bbox from mapillary
    """
    from .get_mapillary_points import get_mapillary_points

    get_mapillary_points(
        bbox,
        geojson_boundaries,
        field_name,
        timestamp_from,
        only_pano,
        organization_ids,
        output_file_point,
        output_file_sequence,
    )


# ============================================
# ========== CREATE CUSTOM SEQUENCES =========
# ============================================
@cli.command("create_custom_sequences")
@click.option("--geojson_points", help="geojson_points", required=True)
@click.option(
    "--output_file_sequence",
    help="Path for custom sequence file",
    default="data/sequences.geojson",
    type=click.Path(),
)
def run_create_custom_sequences(
    geojson_points,
    output_file_sequence,
):
    """
    Script to add Mapillary's URLs to review the images of the sequences
    """
    from .create_custom_sequences import create_custom_sequences

    if validate_geojson_file(geojson_points):
        print("Validations passed. Proceed with processing")
        print("===================================================")
        create_custom_sequences(
            geojson_points,
            output_file_sequence,
        )
    else:
        print("Validation failed. Please correct the input")
        print("===================================================")


# =========================================
# ========== SIMPLIFY POINTS =========
# =========================================
@cli.command("simplify_points")
@click.option(
    "--input_points",
    default="",
    type=str,
    required=True,
    help="Pathfile for geojson input (points)",
)
@click.option(
    "--points_distance",
    required=True,
    help="distance applied for simplifying",
)
@click.option(
    "--output_points",
    default="",
    type=str,
    help="Pathfile for geojson output (points)",
)
def run_simplify_points(input_points, points_distance, output_points):
    """
    Script to simplify points in a sequence according to a given distance
    """
    from .simplify_points import simplify_points

    simplify_points(input_points, points_distance, output_points)


if __name__ == "__main__":
    cli()
