# Geokit-python

Geokit-python is a command-line interface (CLI) tool written in python3, that contains all the basic functionalities for measurements, conversions and operations of geojson, shapefile, osm, xml and others.

# Usage

### tips

you can use `--help` to show options and help

# Chips_ahoy module

## features collection tiles

Script to add tiles and url-tiles to each features in a geojson file.

| COMMAND           | REQUIRED | DESCRIPTION                                       |
| ----------------- | -------- | ------------------------------------------------- |
| --geojson_file    | yes      | path to geojson file                              |
| --zoom            | yes      | zoom to get the tile                              |
| --url_map_service | yes      | tile map service url                              |
| --geojson_output  | yes      | original geojson with the attributes: tile, url   |
| --chuck           | no       | chuck size, default 0                             |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest chips_ahoy fctile --geojson_file <INPUT_GEOJSON> --zoom <ZOOM> --url_map_service <URL_MAP_SERVICE> --geojson_output <OUTPUT_GEOJSON> --chuck <CHUCK_SIZE>
```

## filter for chips-ahoy outputs

Script to separate features tagged as `yes` and  `no` in polygons(tiles) and points.

| COMMAND          | REQUIRED | DESCRIPTION                                 |
| ---------------- | -------- | ------------------------------------------- |
| --geojson_file   | yes      | path to geojson file                        |
| --geojson_output | yes      | Geojson separated in no, yes (tile - point) |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest chips_ahoy filter_chips --geojson_file <INPUT_GEOJSON> --geojson_output <OUTPUT_GEOJSON>
```

# cvat module

## count tags

Get the total of tagged boxes according to their classification.

| COMMAND     | REQUIRED | MULTIPLE | DESCRIPTION           |
| ----------- | -------- | -------- | --------------------- |
| --xml_file  | yes     | yes     | path to cvat xml file |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest cvat count_tag --xml_file <CVAT_XML> 
```

## downsized images

Downsize the images from big size to 512x512. Supports only jpg files.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --img_path   | yes     | path to images folder |
| --output_path | yes    |  path to the output images folder  |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest cvat downsized_imgs --img_path <IMG_FOLDER> --output_path <OUTPUT_FOLDER>
```

## fix ordinal suffixes

Fix ordinal suffixes of xml file.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --xml_input  | yes     | path to xml file |
| --xml_output | yes     | path to the output xml file   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest cvat fix_ordinal_suffixes --xml_input <INPUT_XML> --xml_output <OUTPUT_XML> 
```

## intersection box 

Find the boxes that intersect and are greater than the tolerance, for default tolerance is 70 (70% of the area of the small intersection box).

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --in_file   | yes      | path to cvat xml file |
| --tolerance | no       | tolerance to filter, default: 70.0   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest cvat intersectionbox --in_file <CVAT_XML> --tolerance <TOLERANCE>  > output.csv
```

## npz to xml 

Convert npz to xml format.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --npz_file  | yes      | path to labelMaker npz file |
| --img_path  | yes      | path of the images in CVAT   |
| --img_label | yes      | label image eg : tower   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest cvat npz2xml --npz_file <NPZ> --img_path <IMG_PATH> --img_label <IMG_LABEL>  
```

## Small box 

Find the boxes with an area smaller than the image, for default tolerance is 1 (1% of area image).

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --in_file   | yes      | path to cvat xml file |
| --tolerance | no       | tolerance to filter, default: 1.0   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest cvat smallbox --in_file <CVAT_XML> --tolerance <TOLERANCE>  > output.csv
```

## xml to csv 

Convert xml to csv format.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --xml_file  | yes      | path to cvat xml file |
| --csv_file  | yes      | path to csv file   |
| --full      | no       | use True for obtaining all the attributes of the xml, default: False  |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest cvat xml2csv --xml_file <CVAT_XML> --csv_file <CSV> --full <FULL>
```

## xml to npz 

Convert to xml to npz format.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --xml_file  | yes      | path to cvat xml file |
| --npz_file  | yes      | path to npz file   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest cvat xml2npz --xml_file <CVAT_XML> --npz_file <NPZ>
```

# rl_schoolspoint module

## schools point

find school in [international schools database](https://www.international-schools-database.com) and get point if exist.

| COMMAND | REQUIRED | DESCRIPTION  |
| ------- | -------- | ------------ |
| --city  | yes      | Name of city |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest  rl_schoolspoint --city <CITY_NAME> > output.geojson
```

# geo module

## geo generate id

Addig a key `<id_label>` in the `PROPERTIES` in a geojson file, the value of `id` can start in `1` or `start_count`.
this script can work with `aws - s3` uri.

| COMMAND       | REQUIRED | DESCRIPTION                                                                                       |
| ------------- | -------- | ------------------------------------------------------------------------------------------------- |
| --in_file     | yes      | Path to geojson file                                                                              |
| --id_label    | no       | Name of key to id, default: id                                                                    |
| --id_start    | no       | Value of first id, the next value is its sequence (number), default: 1                            |
| --zeros       | no       | Add zeros at the beginning of the id, until it reaches the specified length. Example: --zeros 3 --> `003` , default : 0|
| --variation   | no       | Type of id (number or uuid), default: number                                                       |
| --output_file | yes      | Path to geojson output file                                                                       |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest  geo generate_id --in_file <GEOJSON_PATH> --id_label <NEW_ID> --id_start 100 --zeros 5  --output_file S3://an-awesome-bucket-name/file.geojson
```

## osm file to new osm file

Removes some attributes of each feature such as: `user`, `version`, `timestamp`, `changeset` and `uid`. So, it returns a new OSM file without these attributes.

| COMMAND         | REQUIRED |DESCRIPTION                           |
| --------------- | -------- | -------------------------------------|
| --input_osm     | yes      | Path to osm file to be processed     |
| --output_osm    | yes      | Path to osm output                   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo osm2new --input_osm <INPUT_OSM> --output_osm <OUTPUT_OSM>
```

## Remove objects with action=delete

Removes the objects with `action=delete` in a osm file.

| COMMAND         | REQUIRED |DESCRIPTION                           |
| --------------- | -------- | -------------------------------------|
| --input_osm     | yes      | Path to osm file to be processed     |
| --output_osm    | yes      | Path to osm output                   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo removeactionosm --input_osm <INPUT_OSM> --output_osm <OUTPUT_OSM>
```

## Features in polygons

Script to add tag `_where` and fields by location `(mode_filter)`. work with aws uri. 

| COMMAND         | REQUIRED  | MULTIPLE |DESCRIPTION                           |
| --------------- | -------- | -------- | -------------------------------------|
| --geojson_in_polygon     | yes      | no       | Path to geojson polygons.  |
| --geojson_in_features    | yes      | no       | Path to geojson features. |
| --tags_polygon           | no       | yes      | Fields in geojson_in_polygon to add features, default: "" |
| --mode_filter            | yes      | no       | Filtering mode:<br/> -include : geometry of feature <br/> -include__centroid: centroid geometry of feature. <br/> - intersect__<% area> : (polygons) is taken in minimum `area` (1, 10, 20, 30, 40, 50, 60, 70, 80, 90) of intersection to consider inside. |
| --mode_output            | yes      | no       | Output mode:<br/> -merged: all features in one file. <br/> -by_location: features in two files, inside and outside.  <br/> -by_polygon_tag: features in multiple files, outside and other by tag. |
| --geojson_out_features    | yes      | no       | Path to geojson features output. |


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo features_in_polygons --geojson_in_polygon <INPUT_GEOJSON>  --geojson_in_features <INPUT_GEOJSON> --tags_polygon tag_1 --tags_polygon tags_2 --mode_filter include --mode_output by_polygon_tag --geojson_out_features <OUTPUT_GEOJSON>
```

## Add attributes geojson

Script to add tag in each feature. work with aws uri. 

| COMMAND         | REQUIRED | MULTIPLE |DESCRIPTION                           |
| --------------- | --------| -------- | -------------------------------------|
| --geojson_input | yes     | no       | Path to geojson polygons.  |
| --tags          | yes     | yes       | Props add features in format: `key=value` |
| --geojson_out   | yes     | no      | Path to geojson features output.|


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo addattributefc --geojson_input <INPUT_GEOJSON>  --tags key1=value1 --tags key2=value2 --geojson_out <OUTPUT_GEOJSON>
```


## Keep attributes geojson

Script to keep keys (properties) in each feature. work with aws uri. 

| COMMAND         | REQUIRED | MULTIPLE|DESCRIPTION                           |
| --------------- | -------- | --------  | -----------------------------------|
| --geojson_input | yes      | no        | Path to geojson polygons.          |
| --keys          | yes      | yes       | Keys to keep.                      |
| --geojson_out   | no       | no        | Path to geojson features output.   |


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo keepattributes --geojson_input <INPUT_GEOJSON>  --keys field1 --keys field2 --keys field3 --geojson_out <OUTPUT_GEOJSON>
```

## geojson to CSV

Script to convert geojson to csv, if `osm_download_link` adds an osm_download_link column per each feature and each link downloads the feature in JOSM.. work with aws uri. 

| COMMAND             | REQUIRED |DESCRIPTION                           |
| ------------------- | -------- | -------------------------------------|
| --geojson_input     | yes      | Path to geojson polygons.  |
| --osm_download_link | no       | Flag to add osm_download_link, default: False|
| --csv_out           | yes      | Path to csv output.|


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo fc2csv --geojson_input <INPUT_GEOJSON>  --osm_download_link --csv_out <OUTPUT_CSV>
```


## difference

Gets the difference of the objects between two geojson files according to a common attribute, this script can work with aws - s3 uri.

| COMMAND         | REQUIRED |DESCRIPTION                           |
| --------------- | -------- | -------------------------------------|
| --geojson_input | yes      | Path to geojson polygons.  |
| --geojson_dif   | yes      | Path to geojson difference to process. |
| --key           | yes      | Could be any of attribute, which is in both files|
| --geojson_output| yes      | Path to geojson output.|


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo difference --geojson_input <INPUT_GEOJSON>   --geojson_dif <INPUT_DIFFERENCE_GEOJSON> --key field_to_filter --geojson_output <OUTPUT_GEOJSON> 
```

## duplicates features

Gets the duplicate objects, identified by a unique attribute or primary key. this script can work with aws - s3 uri.

| COMMAND         | REQUIRED |DESCRIPTION                           |
| --------------- | -------- | -------------------------------------|
| --geojson_input | yes      | Path to geojson polygons.  |
| --key           | yes      | Key to filter. |
| --geojson_output| yes      | Path to geojson output.|


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo duplicatefeatures --geojson_input <INPUT_GEOJSON>  --key field_to_filter  --geojson_output <OUTPUT_GEOJSON>
```

## features filter

Filters features by given property/geometry and it will generate a new geojson file with the filtered features. This script can work with aws - s3 uri.

| COMMAND         | REQUIRED | MULTIPLE | DESCRIPTION                           |
| --------------- | -------- | -------- | -------------------------------------|
| --geojson_input | yes      | no       | Path to geojson polygons.  |
| --mode_filter   | yes      | no       | Mode filter : <br/> -by_properties <br/> -by_properties_strict  <br/> -by_geometry   |
| --props         | yes      | yes      | Props/Geometry to filter. key=value or key=*. |
| --mode_output   | no       | yes      | Mode of file output : <br/> -merged <br/> -by_props  <br/> -by_geometry <br/> default : merged  |
| --geojson_output| yes      | yes      | Path to geojson output.|


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo fc_filter --geojson_input <INPUT_GEOJSON>  --mode_filter by_properties --props key=value --props key1=value2 --mode_output by_props --geojson_output  <OUTPUT_GEOJSON>
```

## features split

Splits up a GeoJSON file into smaller GeoJSON files. This script can work with aws - s3 uri.


| COMMAND          | REQUIRED |DESCRIPTION                  |
| ---------------- | -------- | ---------------------------|
| --geojson_input  | yes      | Path to geojson to process.  |
| --size           | yes     | Size of geometries per split file. |
| --geojson_output | yes      | Path to geojson output.|


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo fc_split --geojson_input <INPUT_GEOJSON>  --size 1000  --geojson_output <OUTPUT_GEOJSON>
```
