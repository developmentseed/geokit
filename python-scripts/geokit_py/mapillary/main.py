"""
Script for mapillary module
Author: @developmentseed
"""

import click

from geokit_py.utils.map_utils import validate_output_path


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
    "--input_aoi",
    type=str,
    required=True,
    help="Path to geojson file of boundaries or bbox in the format 'xMin, yMin, xMax, yMax'",
)
@click.option(
    "--field_name",
    type=str,
    required=False,
    help="A field name from boundaries in the geojson file of boundaries",
)
@click.option(
    "--timestamp_from",
    default=0,
    type=int,
    required=False,
    help="Timestamp to filter images. Value in milliseconds",
)
@click.option(
    "--only_pano",
    default=False,
    type=bool,
    required=False,
    is_flag=True,
    help="Flag to get only pano images",
)
@click.option(
    "--organization_ids",
    type=str,
    required=False,
    help="Organization id to filter images",
)
@click.option(
    "--output_file_point",
    type=click.Path(),
    required=True,
    help="Pathfile for geojson point file",
)
@click.option(
    "--output_file_sequence",
    type=click.Path(),
    required=True,
    help="Pathfile for geojson sequence file",
)
def run_get_mapillary_points(
    input_aoi,
    field_name,
    timestamp_from,
    only_pano,
    organization_ids,
    output_file_point,
    output_file_sequence,
):
    """
    Script to get points and sequence for a bbox or boundaries from mapillary
    """
    from .get_mapillary_points import get_mapillary_points

    def get_aoi_type(input_aoi_):
        if len(input_aoi_.split(",")) == 4:
            return input_aoi_, "", True
        if ".geojson" in input_aoi_:
            return "", input_aoi_, True
        return "", "", False

    bbox, geojson_boundaries, estate = get_aoi_type(input_aoi)

    if estate:
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
    else:
        print("=============================================")
        print(
            "Provide the input_aoi in the correct format:\n"
            "- Geojson file of boundaries or\n "
            "- Bbox in the format 'xMin, yMin, xMax, yMax'\n"
        )
        print("=============================================")


# ============================================
# ========== CREATE CUSTOM SEQUENCES =========
# ============================================
@cli.command("create_custom_sequences")
@click.option(
    "--geojson_points",
    help="geojson_points",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--output_file_sequence",
    help="Path for custom sequence file",
    default="data/custome_sequences.geojson",
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

    if validate_output_path(output_file_sequence):
        create_custom_sequences(geojson_points, output_file_sequence)


# ============================================
# =========== MERGE SEQUENCES ================
# ============================================
@cli.command("merge_sequences")
@click.option(
    "--geojson_input",
    help="Pathfile for geojson input",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--geojson_output",
    help="Pathfile for geojson output",
    default="data/merge_sequences.geojson",
    type=click.Path(),
)
def run_merge_sequences(
    geojson_input,
    geojson_output,
):
    """
    Script to merge sequences and removes duplicate features
    """
    from .merge_sequences import merge_sequences

    if validate_output_path(geojson_output):
        merge_sequences(geojson_input, geojson_output)


# ============================================
# =========== MATCH POINT SEQUENCES ==========
# ============================================
@cli.command("match_point_sequences")
@click.option(
    "--geojson_polygons",
    help="Pathfile for geojson input (polygons)",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--geojson_points",
    help="Pathfile for geojson input (points)",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--geojson_output",
    help="Pathfile for geojson output (points)",
    default="data/match_point_sequences.geojson",
    type=click.Path(),
)
def run_match_point_sequences(
    geojson_polygons,
    geojson_points,
    geojson_output,
):
    """
    Script to filter point in polygons and secuence_id
    """
    from .match_point_sequences import match_point_sequences

    if validate_output_path(geojson_output):
        match_point_sequences(geojson_polygons, geojson_points, geojson_output)


# =========================================
# ========== SIMPLIFY POINTS =========
# =========================================
@cli.command("simplify_points")
@click.option(
    "--input_points",
    type=str,
    required=True,
    help="Pathfile for geojson input (points)",
)
@click.option(
    "--points_distance",
    required=True,
    help="Distance in meters applied for simplifying",
)
@click.option(
    "--output_points",
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
