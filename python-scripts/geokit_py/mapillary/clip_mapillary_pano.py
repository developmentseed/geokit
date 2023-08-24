import click
from geokit_py.utils.utils_images import process_image
from geokit_py.utils.map_utils import read_geojson, write_geojson


def clip_mapillary_pano(
    input_file_points,
    output_file_points,
    output_images_path,
    image_clip_size,
    cube_sides,
):
    """Script to convert 360 images to simple sides images"""

    features = read_geojson(input_file_points)
    output = process_image(features, output_images_path, image_clip_size, cube_sides)
    features = [fea for fea in output if fea is not None]
    write_geojson(output_file_points, features)
