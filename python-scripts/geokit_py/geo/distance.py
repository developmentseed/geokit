from shapely.geometry import shape
from geojson.feature import FeatureCollection as fc
from pyproj import Geod
import json
MEASUREMENT = {
    "meters": {
        "divisor": 1,
        "unit_measur": "m"},
    "kilometers":{
        "divisor": 1000,
        "unit_measur": "km"},
}

def get_distance(geojson_input, unit_measurement, geojson_output):
    """Script to get the distance of each LineString and MultiLineString."""

    with open (geojson_input, encoding="utf8") as gfile:
        features = json.load(gfile).get("features",[])
    geod = Geod(ellps="WGS84")
    distance_total = 0

    for feature in features:
        feature['geom'] = shape(feature.get('geometry',{}))

    for feature in features:
        if ('LineString' or 'MultiLineString') in feature['geom'].geom_type:
            distance = f"distance_{MEASUREMENT.get(unit_measurement).get('unit_measur')}"
            distance_base = round(geod.geometry_length(feature['geom']),3)
            feature["properties"][distance] =round(distance_base/MEASUREMENT.get(unit_measurement).get('divisor'),3)
            distance_total += round(distance_base/MEASUREMENT.get(unit_measurement).get('divisor'),3)

    for feature in features:
        if 'geom' in feature.keys():
            del feature['geom']

    print(f"Total distance: {round(distance_total,3)} {MEASUREMENT.get(unit_measurement).get('unit_measur')}")
    with open(geojson_output, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features), ensure_ascii=False).encode("utf8").decode()
        )
