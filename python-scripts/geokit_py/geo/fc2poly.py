"""geo.fc2poly: Skeleton of a function."""

import json

import geopandas as gpd
from shapely.geometry import box


def fc2poly(geojson_file, poly_file):
    """Generate poly file."""
    poly_name = geojson_file.split("/")[-1].split(".")[0]
    geo_gpd = gpd.read_file(geojson_file)
    geo_gpd = geo_gpd[geo_gpd.geometry.apply(lambda x: "Point" not in x.geom_type)]
    geo_gpd["bbox_"] = geo_gpd.geometry.apply(
        lambda x: list(box(*list(x.bounds)).exterior.coords)
    )
    data_json = json.loads(geo_gpd.to_json())
    poly = [poly_name]
    for k, i in enumerate(data_json.get("features")):
        poly.append(f"{poly_name}__{k}")
        for lat, lng in i["properties"].get("bbox_"):
            poly.append(f"\t{lat}\t{lng}")
        poly.append("END")
    poly.append("END")
    poly_str = "\n".join(poly)
    with open(poly_file, "w+") as src:
        src.write(poly_str)
        src.close()
