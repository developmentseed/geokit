"""mapillary.get_mapillary_points: Skeleton of a function."""

import json

from shapely.geometry import shape

from geokit_py.utils.map_utils import (
    build_mapillary_sequence,
    get_mapillary_points_bbox,
    write_geojson,
)


def add_name_path(path_, name_):
    """Script add a name in a path file"""
    name_extension = path_.strip().split("/")[-1]
    return path_.replace(name_extension, f"{name_}_{name_extension}")


def get_mapillary_points(
    bbox,
    geojson_boundaries,
    field_name,
    timestamp_from,
    only_pano,
    organization_ids,
    output_file_point,
    output_file_sequence,
):
    """Script to get points and sequence for a bbox from mapillary"""
    boundaries = []

    if geojson_boundaries:
        features = json.load(open(geojson_boundaries)).get("features")
        for feature in features:
            props = feature.get("properties")
            name = props.get(field_name, "").strip().replace(" ", "_")
            geom = shape(feature.get("geometry"))
            boundaries.append(
                {
                    "bbox": geom.bounds,
                    "output_file_point": add_name_path(output_file_point, name),
                    "output_file_sequence": add_name_path(output_file_sequence, name),
                    "geom": geom,
                    "name_file": name,
                }
            )
    else:
        boundaries.append(
            {
                "bbox": tuple([float(item.strip()) for item in bbox.split(",")]),
                "output_file_point": output_file_point,
                "output_file_sequence": output_file_sequence,
                "geom": None,
                "name_file": output_file_point.split("/")[-1],
            }
        )
    total_no_pano = 0
    total_pano = 0
    for boundarie in boundaries:
        points = get_mapillary_points_bbox(
            boundarie.get("bbox"),
            only_pano,
            timestamp_from,
            boundarie.get("geom"),
            boundarie.get("name_file"),
        )
        total = len(points)
        pano = [i for i in points if i.get("properties").get("is_pano")]

        print("=" * 10)
        print("city", boundarie.get("name_file"))
        print("total points", total)
        print("pano", len(pano))

        total_pano += len(pano)

        if not only_pano:
            no_pano = [i for i in points if not i.get("properties").get("is_pano")]

            if organization_ids:
                no_pano = [
                    i
                    for i in no_pano
                    if str(i.get("properties").get("organization_id", "--"))
                    in organization_ids.split(",")
                ]

            total_no_pano += len(no_pano)
            print("no pano", len(no_pano))

        write_geojson(
            boundarie.get("output_file_point").replace(".geojson", "__pano.geojson"),
            pano,
        )
        sequences_pano = build_mapillary_sequence(pano)
        print("total sequences pano", len(sequences_pano))

        write_geojson(
            boundarie.get("output_file_sequence").replace(".geojson", "__pano.geojson"),
            sequences_pano,
        )

        if not only_pano:
            write_geojson(
                boundarie.get("output_file_point").replace(
                    ".geojson", "__no__pano.geojson"
                ),
                no_pano,
            )
            sequences_no_pano = build_mapillary_sequence(no_pano)
            print("total sequences no pano", len(sequences_no_pano))

            write_geojson(
                boundarie.get("output_file_sequence").replace(
                    ".geojson", "__no__pano.geojson"
                ),
                sequences_no_pano,
            )

    print("=" * 10)
    print("=" * 10)
    print("pano", total_pano)
    print("no pano", total_no_pano)
    print("=======")
