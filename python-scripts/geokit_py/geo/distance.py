"""geo.distance: Skeleton of a function."""

import json

from geojson.feature import FeatureCollection as fc
from pyproj import Geod
from shapely.geometry import shape

MEASUREMENT_D = {
    "meters": {"divisor": 1, "unit_measur": "m"},
    "kilometers": {"divisor": 1000, "unit_measur": "km"},
}


def get_distance(geojson_input, unit_measurement, geojson_output):
    """Script to get the distance of each LineString and MultiLineString."""

    with open(geojson_input, encoding="utf8") as gfile:
        features = json.load(gfile).get("features", [])
    geod = Geod(ellps="WGS84")
    distance_total = 0

    for feature in features:
        geom = shape(feature.get("geometry", {}))
        if "LineString" in geom.geom_type:
            distance = (
                f"distance_{MEASUREMENT_D.get(unit_measurement).get('unit_measur')}"
            )
            distance_base = abs(round(geod.geometry_length(geom), 3))
            distance_num = round(
                distance_base / MEASUREMENT_D.get(unit_measurement).get("divisor"), 3
            )
            feature["properties"][distance] = distance_num
            distance_total += distance_num

    print(
        f"Total distance: {round(distance_total, 3)} {MEASUREMENT_D.get(unit_measurement).get('unit_measur')}"
    )
    with open(geojson_output, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features), ensure_ascii=False).encode("utf8").decode()
        )
