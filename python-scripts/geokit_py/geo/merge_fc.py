"""geo.merge_fc: Skeleton of a function."""
import itertools
import json

from geojson.feature import FeatureCollection as fc
from geokit_py.utils.code import get_list_files_folder
from joblib import Parallel, delayed
from smart_open import open
from tqdm import tqdm


def fetch_features(geojson_paths):
    """Fetch data from paths"""

    def fetch_data(file_path):
        """Fetch data."""
        if not file_path:
            return {"file_name": "error", "data": []}
        data_ = json.load(open(file_path)).get("features", [])
        return {"file_name": file_path, "data": data_}

    new_feature_includes = Parallel(n_jobs=-1)(
        delayed(fetch_data)(feature)
        for feature in tqdm(geojson_paths, desc="fetch data ")
    )
    # print data len
    for i in new_feature_includes:
        print(f"{i['file_name']}:  \t {str(len(i['data'])).zfill(4)}")

    data_clean = [i["data"] for i in new_feature_includes]
    return list(itertools.chain(*data_clean))


def merge_features(geojson_inputs, folder_path, recursive, geojson_output):
    """Script to merge features."""
    files_folder = get_list_files_folder(folder_path, recursive, ".geojson")
    features_path = [*geojson_inputs, *files_folder]
    print("==================")
    features_ = fetch_features(features_path)
    print("==================")
    print(f"total output: \t{str(len(features_)).zfill(4)}")
    print("==================")
    with open(geojson_output, "w") as f:
        f.write(json.dumps(fc(features_), ensure_ascii=False).encode("utf8").decode())
