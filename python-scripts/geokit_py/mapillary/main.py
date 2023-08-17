"""
Script for mapillary module
Author: @developmentseed
"""

import click


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


if __name__ == "__main__":
    cli()
