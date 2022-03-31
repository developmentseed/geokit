from geojson.feature import FeatureCollection as fc
import json
from pyproj import Geod
from shapely.geometry import shape
MEASUREMENT = {
    "square_meters": {
        "divisor": 1,
        "unit_measur": "m2"},
    "hectares": {
        "divisor": 10000,
        "unit_measur": "ha"},
    "square_kilometers":{
        "divisor": 1000000,
        "unit_measur": "km2"},
}

def get_feature_area(geojson_input, unit_measurement,geojson_output):
    """Script to get the area of each polygon feature."""
    with open (geojson_input, encoding="utf8") as gfile:
        features = json.load(gfile).get("features",[])
    geod = Geod(ellps="WGS84")
    area_total = 0

    for feature in features:
        feature['geom'] = shape(feature.get('geometry',{}))
    for feature in features:
        if 'Polygon' in feature['geom'].geom_type:
            area = f"area_{MEASUREMENT.get(unit_measurement).get('unit_measur')}"
            area_base = round(geod.geometry_area_perimeter(feature['geom'])[0],3)
            feature["properties"][area]  = round(area_base/MEASUREMENT.get(unit_measurement).get("divisor"),3)
            area_total += round(area_base/MEASUREMENT.get(unit_measurement).get("divisor"),3)

    for feature in features:
        if 'geom' in feature.keys():
            del feature['geom']

    print(f"Area total: {round(area_total,3)} {MEASUREMENT.get(unit_measurement).get('unit_measur')}")
    with open(geojson_output, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features), ensure_ascii=False).encode("utf8").decode()
        )
