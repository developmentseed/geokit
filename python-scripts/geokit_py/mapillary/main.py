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
)
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


# ============================================
# =========== MERGE SEQUENCES ================
# ============================================
@cli.command("merge_sequences")
@click.option(
    "--geojson_input",
    help="Pathfile for geojson input",
    type=str,
)
@click.option(
    "--geojson_output",
    help="Pathfile for geojson output",
    type=str,
)
def run_merge_sequences(
    geojson_input,
    geojson_output,
):
    """
    Script to merge sequences and removes duplicate features
    """
    from .merge_sequences import merge_sequences

    if validate_geojson_file(geojson_input):
        print("Validations passed. Proceed with processing")
        print("===================================================")
        merge_sequences(geojson_input, geojson_output)
    else:
        print("Validation failed. Please correct the input")
        print("===================================================")


# =========================================
# ========== SIMPLIFY SEQUENCES =========
# =========================================


@cli.command("simplify_sequence")
@click.option(
    "--geojson_input",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    required=True,
    help="Pathfile for geojson input",
)
@click.option(
    "--buffer",
    type=float,
    required=True,
    help="Input the buffer size",
)
@click.option(
    "--geojson_out",
    type=click.Path(),
    help="Output geojson file",
)
def run_simplify_sequence(geojson_input, buffer, geojson_out):
    """
    Script to simplify sequences by buffer
    """
    from .simplify_sequence import simplify_sequence

    simplify_sequence(geojson_input, buffer, geojson_out)


# =========================================
# ========== SIMPLIFY POINTS =========
# =========================================
@cli.command("simplify_points")
@click.option(
    "--input_points",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
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
    type=click.Path(),
    help="Pathfile for geojson output (points)",
)
def run_simplify_points(input_points, points_distance, output_points):
    """
    Script to simplify points in a sequence according to a given distance
    """
    from .simplify_points import simplify_points

    simplify_points(input_points, points_distance, output_points)


# =========================================
# ========== CLIP MAPILLARY PANO ==========
# =========================================


@cli.command("clip_mapillary_pano")
@click.option(
    "--input_file_points",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    required=True,
    help="Input geojson file of Mapillary points",
)
@click.option(
    "--image_clip_size",
    type=int,
    default=1024,
    help="Image size for each image to be clipped",
)
@click.option(
    "--output_images_path",
    type=click.Path(),
    help="Output images path",
)
@click.option(
    "--output_file_points",
    type=click.Path(),
    help="Output points for images that were processed",
)
@click.option(
    "--cube_sides",
    default="right,left",
    help="Sides of the image to save",
)
def run_clip_mapillary_pano(
    input_file_points,
    output_file_points,
    output_images_path,
    image_clip_size,
    cube_sides,
):
    """
    Script to convert 360 images to simple sides images
    """
    from .clip_mapillary_pano import clip_mapillary_pano

    clip_mapillary_pano(
        input_file_points,
        output_file_points,
        output_images_path,
        image_clip_size,
        cube_sides,
    )


if __name__ == "__main__":
    cli()
