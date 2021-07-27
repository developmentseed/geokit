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
| --geojson_output  | no       | original geojson with the attributes: tile, url   |
| --chuck           | no       | chuck size                                        |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python chips_ahoy fctile --geojson_file <INPUT_GEOJSON> --zoom <ZOOM> --url_map_service <URL_MAP_SERVICE> --geojson_output <OUTPUT_GEOJSON> --chuck <CHUCK_SIZE>
```

## filter for chips-ahoy outputs

Script to separate features tagged as `yes` and  `no` in polygons(tiles) and points.

| COMMAND          | REQUIRED | DESCRIPTION                                 |
| ---------------- | -------- | ------------------------------------------- |
| --geojson_file   | yes      | path to geojson file                        |
| --geojson_output | no       | Geojson separated in no, yes (tile - point) |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python chips_ahoy filter_chips --geojson_file <INPUT_GEOJSON> --geojson_output <OUTPUT_GEOJSON>
```

# cvat module

## count tags

Get the total of tagged boxes according to their classification.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --xml_file  | yes     | path to cvat xml file |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python cvat count_tag --xml_file <CVAT_XML> 
```

## downsized images

Downsize the images from big size to 512x512. Supports only jpg files.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --img_path   | yes     | path to images folder |
| --output_path | yes    |  path to the output images folder  |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python cvat downsized_imgs --img_path <IMG_FOLDER> --output_path <OUTPUT_FOLDER>
```

## fix ordinal suffixes

Fix ordinal suffixes of xml file.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --xml_input  | yes     | path to xml file |
| --xml_output | yes     | path to the output xml file   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python cvat fix_ordinal_suffixes --xml_input <INPUT_XML> --xml_output <OUTPUT_XML> 
```

## intersection box 

Find the boxes that intersect and are greater than the tolerance, for default tolerance is 70 (70% of the area of the small intersection box).

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --in_file   | yes      | path to cvat xml file |
| --tolerance | no       | tolerance to filter   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python cvat intersectionbox --in_file <CVAT_XML> --tolerance <TOLERANCE>  > output.csv
```

## npz to xml 

Convert npz to xml format.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --npz_file  | yes      | path to labelMaker npz file |
| --img_path  | yes      | path of the images in CVAT   |
| --img_label | yes      | label image eg : tower   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python cvat npz2xml --npz_file <NPZ> --img_path <IMG_PATH> --img_label <IMG_LABEL>  
```

## Small box 

Find the boxes with an area smaller than the image, for default tolerance is 1 (1% of area image).

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --in_file   | yes      | path to cvat xml file |
| --tolerance | no       | tolerance to filter   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python cvat smallbox --in_file <CVAT_XML> --tolerance <TOLERANCE>  > output.csv
```

## xml to csv 

Convert xml to csv format.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --xml_file  | yes      | path to cvat xml file |
| --csv_file  | yes      | path to csv file   |
| --full      | no       | use True for obtaining all the attributes of the xml   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python cvat xml2csv --xml_file <CVAT_XML> --csv_file <CSV> --full <FULL>
```

## xml to npz 

Convert to xml to npz format.

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --xml_file  | yes      | path to cvat xml file |
| --npz_file  | yes      | path to npz file   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python cvat xml2npz --xml_file <CVAT_XML> --npz_file <NPZ>
```

# rl_schoolspoint module

## schools point

find school in [international schools database](https://www.international-schools-database.com) and get point if exist.

| COMMAND | REQUIRED | DESCRIPTION  |
| ------- | -------- | ------------ |
| --city  | yes      | name of city |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python  rl_schoolspoint --city <CITY_NAME> > output.geojson
```

# geo module

## geo generate id

Addig a key `<id_label>` in the `PROPERTIES` in a geojson file, the value of `id` can start in `1` or `start_count`.
this script can work with `aws - s3` uri.

| COMMAND       | REQUIRED | DESCRIPTION                                                                                       |
| ------------- | -------- | ------------------------------------------------------------------------------------------------- |
| --in_file     | yes      | path to geojson file                                                                              |
| --id_label    | no       | name of key to id                                                                                 |
| --id_start    | no       | value of first id, the next value is its sequence (number)                                        |
| --zeros       | no       | add zeros at the beginning of the id, until it reaches the specified length. Example: --zeros 3 --> `003` |
| --variation   | no       | type of id (number or uuid), default=number                                                       |
| --output_file | yes      | Path to geojson output file                                                                       |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python  geo generate_id --in_file <GEOJSON_PATH> --id_label <NEW_ID> --id_start 100 --zeros 5  --output_file S3://an-awesome-bucket-name/file.geojson
```

## osm file to new osm file

Removes some attributes of each feature such as: `user`, `version`, `timestamp`, `changeset` and `uid`. So, it returns a new OSM file without these attributes.

| COMMAND         | REQUIRED |DESCRIPTION                           |
| --------------- | -------- | -------------------------------------|
| --input_osm     | yes      | Path to osm file to be processed     |
| --output_osm    | yes      | Path to osm output                   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python geo osm2new --input_osm <INPUT_OSM> --output_osm <OUTPUT_OSM>
```

## Remove objects with action=delete

Removes the objects with `action=delete` in a osm file.

| COMMAND         | REQUIRED |DESCRIPTION                           |
| --------------- | -------- | -------------------------------------|
| --input_osm     | yes      | Path to osm file to be processed     |
| --output_osm    | yes      | Path to osm output                   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python geo removeactionosm --input_osm <INPUT_OSM> --output_osm <OUTPUT_OSM>
```
