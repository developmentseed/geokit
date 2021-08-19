"""geo.generateid: Skeleton of a function."""

import geopandas as gpd
from smart_open import open


def osm_download_link_(bounds):
    """Generate osm link."""
    (minx, miny, maxx, maxy) = bounds
    return f"http://127.0.0.1:8111/load_and_zoom?left={minx}&bottom={miny}&right={maxx}&top={maxy}"


def fc2csv(in_file, osm_download_link, output_file):
    """Convert geojson to csv."""
    with open(in_file, "r", encoding="utf8") as gfile:
        gdf = gpd.read_file(gfile)
    if osm_download_link:
        osm_download_link_data = gdf.apply(
            lambda y: osm_download_link_(y.geometry.bounds), axis=1
        )
        gdf.insert(
            gdf.columns.__len__() - 1, "osm_download_link", osm_download_link_data
        )

    with open(output_file, "w") as out_geo:
        out_geo.write(gdf.to_csv(index=False))
