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


# =========================================
# ============== GENERATE ID ==============
# =========================================


@cli.command("generate_id")
@click.option(
    "--in_file",
    required=True,
    type=str,
    help="Path to geojson file to be processed.",
)
@click.option("--id_label", default="id", type=str, required=False, help="key for id")
@click.option(
    "--id_start", default=1, type=int, required=False, help="value to start id"
)
@click.option(
    "--zeros",
    default=0,
    type=int,
    required=False,
    help="adds zeros at the beginning of the id",
)
@click.option(
    "--variation",
    default="NUMBER",
    required=False,
    type=click.Choice(["NUMBER", "UUID"], case_sensitive=False),
    help="type of id (number or uuid)",
)
@click.option(
    "--output_file", required=True, type=str, help="Path to geojson output file"
)
def run_generate_id(in_file, id_label, id_start, zeros, variation, output_file):
    """
    Addig a key <id_label> in the PROPERTIES in a geojson file, the value of id can start in 1 or start_count. This script can work with `aws - s3` uri.
    """
    from .generateid import generateid

    generateid(in_file, id_label, id_start, zeros, variation, output_file)


# =========================================
# ============== OSM 2 NEW  ==============
# =========================================


@cli.command("osm2new")
@click.option(
    "--input_osm", required=True, type=str, help="Path to osm file to be processed."
)
@click.option("--output_osm", required=True, type=str, help="Path to osm output.")
def run_osm2new(input_osm, output_osm):
    """
    Removes some attributes of each feature such as: user, version, timestamp, changeset and uid.
    So it returns a new OSM file without these attributes, this script can work with aws - s3 uri.
    """
    from .osm2new import osm2new

    osm2new(input_osm, output_osm)


# =================================================
# ============== REMOVE ACTIONS OSM  ==============
# =================================================


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


# ==================================================
# ============== FEATURES IN POLYGONS ==============
# ===================================================


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
    type=click.Choice(
        [
            "include",
            "include__centroid",
            # intersect range
            "intersect__1",
            "intersect__10",
            "intersect__20",
            "intersect__30",
            "intersect__40",
            "intersect__50",
            "intersect__60",
            "intersect__70",
            "intersect__80",
            "intersect__90",
        ],
        case_sensitive=True,
    ),
    help="mode of filter, default: include__centroid",
)
@click.option(
    "--mode_output",
    required=True,
    type=click.Choice(["merged", "by_location", "by_polygon_tag"], case_sensitive=True),
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
    Script to add tag '_where' and fields by location (mode_filter). this script can work with aws - s3 uri.
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


# ===============================================
# ============== ADD ATTRIBUTES FC ==============
# ===============================================


@cli.command("addattributefc")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--tags",
    required=True,
    type=str,
    multiple=True,
    help="props add features in format: key=value",
)
@click.option(
    "--geojson_out",
    required=True,
    type=str,
    help="Path to geojson features output.",
)
def run_addattributefc(
    geojson_input,
    tags,
    geojson_out,
):
    """
    Add tags in each feature, this script can work with aws - s3 uri.
    """
    from .addattributefc import add_attribute_fc

    add_attribute_fc(
        geojson_input,
        tags,
        geojson_out,
    )


# ===============================================
# ============== KEEP ATTRIBUTES  ===============
# ================================================


@cli.command("keepattributes")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--keys",
    required=True,
    type=str,
    default=[],
    multiple=True,
    help="keys to keep",
)
@click.option(
    "--geojson_out",
    required=True,
    type=str,
    help="Path to geojson features output.",
)
def run_keepattributes(
    geojson_input,
    keys,
    geojson_out,
):
    """
    Keep only keys add, remove others, this script can work with aws - s3 uri.
    """
    from .keepattributes import keep_attributes

    keep_attributes(
        geojson_input,
        keys,
        geojson_out,
    )


# ===============================================
# ============== FC 2 CSV   =====================
# ================================================


@cli.command("fc2csv")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--osm_download_link",
    required=False,
    is_flag=True,
    default=False,
    help="add osm_download_link",
)
@click.option(
    "--csv_out",
    required=True,
    type=str,
    help="Path to csv output.",
)
def run_fc2csv(
    geojson_input,
    osm_download_link,
    csv_out,
):
    """
    Convert geojson to csv, this script can work with aws - s3 uri.
    """
    from .fc2csv import fc2csv

    fc2csv(
        geojson_input,
        osm_download_link,
        csv_out,
    )


# ===============================================
# ============== DIFFERENCE =====================
# ================================================


@cli.command("difference")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--geojson_dif",
    required=True,
    type=str,
    help="Path to geojson difference to process.",
)
@click.option(
    "--key",
    required=True,
    help="Could be any of attribute, which is in both files.",
)
@click.option(
    "--geojson_output", required=True, type=str, help="Path to geojson output."
)
def run_difference(geojson_input, geojson_dif, key, geojson_output):
    """
    Gets the difference of the objects between two geojson files according to a common attribute, this script can work with aws - s3 uri.
    """
    from .difference_by_tag import difference_by_tag

    difference_by_tag(geojson_input, geojson_dif, key, geojson_output)


# ===============================================
# ============== DUPLICATES BY TAG ==============
# ================================================


@cli.command("duplicatefeatures")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--key",
    required=True,
    help="key to filter.",
)
@click.option(
    "--geojson_output", required=True, type=str, help="Path to geojson output."
)
def run_duplicatefeatures(geojson_input, key, geojson_output):
    """
    Gets the duplicate objects, identified by a unique attribute or primary key. this script can work with aws - s3 uri.
    """
    from .duplicatefeatures_by_tag import duplicate_features_by_tag

    duplicate_features_by_tag(geojson_input, key, geojson_output)


# ===============================================
# ============== FILTER PROP / GEOMETRY ==========
# ===============================================


@cli.command("fc_filter")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--mode_filter",
    required=True,
    type=click.Choice(
        ["by_properties", "by_properties_strict", "by_geometry"], case_sensitive=True
    ),
    help="Mode filter.",
)
@click.option(
    "--props",
    required=True,
    multiple=True,
    help="Props/Geometry to filter. key=value or key=*.",
)
@click.option(
    "--mode_output",
    required=False,
    default="merged",
    type=click.Choice(["merged", "by_props", "by_geometry"], case_sensitive=True),
    help="mode of file output.",
)
@click.option(
    "--geojson_output", required=True, type=str, help="Path to geojson output."
)
def run_filter_by(geojson_input, props, mode_filter, mode_output, geojson_output):
    """
    Filters features by given property/geometry and it will generate a new geojson file with the filtered features. This script can work with aws - s3 uri.
    """
    from .filter_by_props_geometry import filter_by

    filter_by(geojson_input, props, mode_filter, mode_output, geojson_output, False)


# ===============================================
# ============== SPLIT GEOJSON ==================
# ===============================================


@cli.command("fc_split")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--size",
    required=True,
    type=int,
    help="Size of geometries per split file.",
)
@click.option(
    "--geojson_output", required=True, type=str, help="Path to geojson output."
)
def run_fc_split(geojson_input, size, geojson_output):
    """
    Splits up a GeoJSON file into smaller GeoJSON files. This script can work with aws - s3 uri.
    """
    from .fc_split import fc_split

    fc_split(geojson_input, size, geojson_output, False)


# ===============================================
# ============== CLIP GEOJSON ==================
# ===============================================


@cli.command("clip")
@click.option("--geojson_input", help="geojson input", type=str)
@click.option("--geojson_boundary", help="geojson boundary", type=str)
@click.option("--geojson_output", help="geojson output", type=str)
def run_clip(geojson_input, geojson_boundary, geojson_output):
    """Script to clip features."""
    from .clip import clip

    clip(geojson_input, geojson_boundary, geojson_output)


# ===============================================
# ============== MERGE GEOJSON ==================
# ===============================================


@cli.command("merge_fc")
@click.option(
    "--geojson_inputs", help="geojson input", type=str, required=False, multiple=True
)
@click.option(
    "--folder_path",
    help="folder geojson path",
    type=str,
    required=False,
)
@click.option(
    "--recursive",
    help="flag search under folders",
    is_flag=True,
    default=False,
)
@click.option("--geojson_output", help="geojson output", type=str)
def run_merge_fc(geojson_inputs, folder_path, recursive, geojson_output):
    """Script to merge multiple featurecollections."""
    from .merge_fc import merge_features

    merge_features(geojson_inputs, folder_path, recursive, geojson_output)


# ===============================================
# ============== GET DISTANCE PER EACH FEATURE==============
# ===============================================

from .distance import MEASUREMENT

@cli.command("distance")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--unit_measurement",
    required=True,
    type=click.Choice(list(MEASUREMENT.keys()), case_sensitive=True),
    help="Unit of distance measurement",
)
@click.option(
    "--geojson_output",
    required=True,
    type=str,
    help="Path to geojson features output.",
)
def run_get_distance(
    geojson_input,
    unit_measurement,
    geojson_output,
):
    """
    Get the distance of each LineString and MultiLineString.
    """
    from .distance import get_distance

    get_distance(
        geojson_input,
        unit_measurement,
        geojson_output,
    )

# ===============================================
# ============== RENAME KEY ==============
# ===============================================

@cli.command("renamekey")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--old_key",
    required=True,
    type=str,
    help="Old key for rename",
)
@click.option(
    "--new_key",
    required=True,
    type=str,
    help="New name for the key",
)
@click.option(
    "--geojson_output",
    required=True,
    type=str,
    help="Path to geojson features output.",
)
def run_renamekey(
    geojson_input,
    old_key,
    new_key,
    geojson_output,
):
    """
    Script to rename a key of the features
    """
    from .renamekey import rename_key

    rename_key(
        geojson_input,
        old_key,
        new_key,
        geojson_output,
    )

# ===============================================
# ============== DELETE NULLS ==============
# ===============================================

@cli.command("deletenulls")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--geojson_output",
    required=True,
    type=str,
    help="Path to geojson features output.",
)
@click.option(
    "--delete_feat",
    required=False,
    default=False,
    help="Delete those features that have an attribute with a null value",
)

def run_deletenulls(
    geojson_input,
    geojson_output,
    delete_feat,
):
    """
    Script to delete the attributes that have a null value.
    """
    from .deletenulls import delete_null_values

    delete_null_values(
        geojson_input,
        geojson_output,
        delete_feat,
    )

# ===============================================
# ============== GET AREA PER EACH FEATURE ==============
# ===============================================
from .featurearea import MEASUREMENT

@cli.command("featurearea")
@click.option(
    "--geojson_input", required=True, type=str, help="Path to geojson to process."
)
@click.option(
    "--unit_measurement",
    required=True,
    type=click.Choice(list(MEASUREMENT.keys()), case_sensitive=True),
    help="Unit of area measurement",
)
@click.option(
    "--geojson_output",
    required=True,
    type=str,
    help="Path to geojson features output.",
)

def run_featurearea(
    geojson_input,
    unit_measurement,
    geojson_output,
):
    """
    Script to get the area of each polygon feature.
    """
    from .featurearea import get_feature_area

    get_feature_area(
        geojson_input,
        unit_measurement,
        geojson_output,
    )

if __name__ == "__main__":
    cli()
