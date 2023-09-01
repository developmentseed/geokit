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
| --is_super_tile   | no       | Flag add neighbors tiles, default False           |
```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest chips_ahoy fctile --geojson_file <INPUT_GEOJSON> --zoom <ZOOM> --url_map_service <URL_MAP_SERVICE> --geojson_output <OUTPUT_GEOJSON> --chuck <CHUCK_SIZE>
```

## filter for chips-ahoy outputs

Script to separate features tagged as `yes` and  `no` in polygons(tiles) and points.

| COMMAND          | REQUIRED | DESCRIPTION                                 |
| ---------------- | -------- | ------------------------------------------- |
| --geojson_file   | yes      | path to geojson file                        |
| --geojson_output | yes      | Geojson separated in no, yes (tile - point) |
| --clean_fields   | no       | Flag option - for cleaning chips-ahoy fields|

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest chips_ahoy filter_chips --geojson_file <INPUT_GEOJSON> --geojson_output <OUTPUT_GEOJSON> --clean_fields
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

## clip features

Script to clip features. This script can work with aws - s3 uri.

| COMMAND          | REQUIRED |DESCRIPTION                  |
| ---------------- | -------- | ---------------------------|
| --geojson_input  | yes      | Path to geojson to process.  |
| --geojson_boundary | yes    | Path to geojson boundary. |
| --geojson_output | yes      | Path to geojson output.|


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo clip --geojson_input  <INPUT_GEOJSON> --geojson_boundary  <BOUNDARY_GEOJSON> --geojson_output  <OUTPUT_GEOJSON>

```


## merge features

Script to merge multiple features. This script can work with aws - s3 uri.

| COMMAND          | REQUIRED |MULTIPLE |DESCRIPTION                  |
| ---------------- | -------- |  -------- |---------------------------|
| --geojson_input  | no      |  yes      |Path to geojson to process.  |
| --folder_path  | no      |  no      |Path to folders with geojson files.  |
| --recursive  | no      |  no      |Flag to search under folder_path, default: False |
| --geojson_output | yes      |  no      |Path to geojson output.|


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest geo merge_fc --geojson_inputs <INPUT_GEOJSON>  --geojson_inputs <INPUT_GEOJSON>   --geojson_inputs <INPUT_GEOJSON>  --folder_path <FOLDER_S3> --recursive --geojson_output <OUTPUT_GEOJSON>
```


# Mapillary module
Useful scripts to get data from [Mapillary](https://www.mapillary.com/app/).

You can export you mapillary token by:

```
export MAPILLARY_ACCESS_TOKEN="MLY|..."
```

## get mapillary points
Script to get points and sequence for a bbox or boundaries from mapillary.

| COMMAND                | REQUIRED | DESCRIPTION                                                                       |
|------------------------|-------|-----------------------------------------------------------------------------------|
| --input_aoi            | yes   | Path to geojson file of boundaries or bbox in the format 'xMin, yMin, xMax, yMax' |
| --field_name           | no    | A field name from the GeoJSON boundaries                                          |
| --timestamp_from(*)    | no    | Timestamp to filter images. Value in milliseconds                                 |
| --only_pano            | no    | Filter only panoramic image                                                       |
| --organization_ids(**) | no    | Filter by organization id from Mapillary                                          |
| --output_file_point    | no    | Pathfile for geojson point file                                                   |
| --output_file_sequence | no   | Pathfile for geojson sequence file                                                |

( * ) Convert the human date to timestamp (milliseconds) [here](https://www.epochconverter.com/). 
( ** ) Download a short area in order to recognize the organization id, then check out if the organization id belongs to the required organization `https://graph.mapillary.com/$ORGANIZATION_ID?access_token=$TOKEN&fields=name`.

```
docker run --rm -v ${PWD}:/mnt/data -e MAPILLARY_ACCESS_TOKEN=${MAPILLARY_ACCESS_TOKEN} -it developmentseed/geokit:python.latest mapillary \
    get_mapillary_points \
    --input_aoi=<INPUT_GEOJSON> \
    --field_name=area \
    --timestamp_from=1651366800000 \
    --organization_ids=1805883732926354 \
    --output_file_point=<OUTPUT_GEOJSON_POINTS> \
    --output_file_sequence=<OUTPUT_GEOJSON_SEQUENCES>
```

## create custom sequences
It adds URLs to review the images of the sequences.

| COMMAND                 | REQUIRED | DESCRIPTION                                              |
| -----------------       | -------- | -------------------------------------------------        |
| --geojson_points        | yes      | point file path                                          |
| --output_file_sequence  | no       | custom sequence file path                                |


```
docker run --rm -v ${PWD}:/mnt/data -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed geokit:python.latest mapillary create_custom_sequences --geojson_points <INPUT_GEOJSON> --output_file_sequence <OUTPUT_GEOJSON>
```

In Mapillary, many sequences have a frontal view (road) of street-view imagery. These sequences are not useful for us when we want to label the facade building or lots, so we can remove them.

In order to delete unnecessary sequences, it is necessary to have the generated custom sequence files and upload them to the tool. We have 2 tools that help us to do it:
1. A plugin in JOSM to be able to see an image of a sequence and to be able to delete it if necessary (download it from s3://ds-data-projects/JOSM/osm-obj-info.jar). 

2. An [app](https://filter_sequences.surge.sh/) that allows us to load GeoJSON files and view random images of a sequence, it allows us to delete sequences by marking with a check.

## merge sequences
It merges sequences and removes duplicate values.

| COMMAND                 | REQUIRED | DESCRIPTION                                              |
| -----------------       | -------- | -------------------------------------------------        |
| --geojson_input         | yes      | checked sequence file path                               |
| --geojson_output        | no       | merge sequence file path                                 |

```
docker run --rm -v ${PWD}:/mnt/data -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed geokit:python.latest mapillary merge_sequences --geojson_input <INPUT_GEOJSON> --geojson_output <OUTPUT_GEOJSON>
```

## simplify sequences
Script to simplify mapillary sequences by buffer.

| COMMAND       | REQUIRED | DESCRIPTION                 |
| ------------- |----------|-----------------------------|
| --geojson_input     | yes      | Pathfile for geojson input  |
| --buffer    | yes      | Buffer size for simplifying |
| --geojson_out    | no       | Pathfile for geojson output |


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest mapillary \
    simplify_sequence \
    --geojson_input=<INPUT_GEOJSON> \
    --buffer=0.000015 \
    --geojson_out=<OUTPUT_GEOJSON>
```

## match point sequences
It filters points inside polygons.

| COMMAND                 | REQUIRED | DESCRIPTION                                              |
| -----------------       | -------- | -------------------------------------------------        |
| --geojson_polygons      | yes      | filter buffer file path (polygons)                       |
| --geojson_points        | yes      | points file path (points)                                |
| --geojson_output        | no       | filter check file path (points)                          |

```
docker run --rm -v ${PWD}:/mnt/data -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed geokit:python.latest mapillary match_point_sequences --geojson_polygons <INPUT_GEOJSON> --geojson_points <INPUT_GEOJSON> --geojson_output <OUTPUT_GEOJSON>
```

## simplify points
Script to simplify points in a mapillary sequence according to a given distance in meters.

| COMMAND       | REQUIRED | DESCRIPTION                                                                                       |
| ------------- |----------| ------------------------------------------------------------------------------------------------- |
| --input_points     | yes      | Pathfile for geojson input (points)                                                                              |
| --points_distance    | yes      | Distance in meters applied for simplifying                                                                    |
| --output_points    | no       | Pathfile for geojson output (points)                            |


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python.latest mapillary \
    simplify_points \
    --input_points=<INPUT_GEOJSON> \
    --points_distance=4 \
    --output_points=<OUTPUT_GEOJSON>
```

## download images
It downloads the Mapillary images
| COMMAND                 | REQUIRED | DESCRIPTION                                              |
| -----------------       | -------- | -------------------------------------------------        |
| --input_file_points     | yes      | Mapillary points file path                               | 
| --output_images_path    | no       | output images path                                       |
| --output_file_points    | no       | output points for images                                 |

```
docker run --rm -v ${PWD}:/mnt/data -e MAPILLARY_ACCESS_TOKEN=$MAPILLARY_ACCESS_TOKEN -it developmentseed geokit:python.latest mapillary download_mapillary_imgs --input_file_points <INPUT_GEOJSON> --output_images_path <OUTPUT_IMAGES PATH> --output_file_points <OUTPUT_GEOJSON>
```


