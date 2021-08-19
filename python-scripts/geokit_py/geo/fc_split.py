"""
Script for add tile and url in features.

Author: @developmentseed
"""
import json
from itertools import islice

from geojson import FeatureCollection as fc
from smart_open import open


def buils_chunk(it, size_):
    """Return list of chuks by size."""
    it = iter(it)
    return iter(lambda: tuple(islice(it, size_)), ())


def fc_split(geojson_input, size, geojson_output, is_test):
    """Script for split geojson in chucks."""

    with open(geojson_input, encoding="utf8") as gfile:
        features = json.load(gfile).get("features", [])

    print(f"Total features : {len(features)}")
    if is_test:
        return list(buils_chunk(features, size))

    for k, i in enumerate(list(buils_chunk(features, size))):
        print(f"File  {str(k).zfill(3)} : {len(i)}")

        with open(
            geojson_output.replace(".geojson", f"__{str(k).zfill(3)}.geojson"), "w"
        ) as out_geo:
            out_geo.write(json.dumps(fc(i), ensure_ascii=False).encode("utf8").decode())
