from geojson.feature import FeatureCollection as fc
import json

def rename_key(geojson_input, old_key, new_key, geojson_output):
    """Script to rename a key of the features"""
    with open (geojson_input, encoding="utf8") as gfile:
        features_ = json.load(gfile).get("features",[])

        for i in features_:
            properties = i.get('properties','')
            old_key_ = properties.get(old_key,'')
            if old_key_:
                properties[new_key] = properties[old_key]
                del properties[old_key]

    with open(geojson_output, "w") as out_geo:
        out_geo.write(
            json.dumps(fc(features_), ensure_ascii=False).encode("utf8").decode()
        )
