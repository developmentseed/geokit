# Geokit-python

Geokit-python is a command-line interface (CLI) tool written in python3, that contains all the basic functionalities for measurements, conversions and operations of geojson, shapefile, osm, xml and others.

# Usage

### tips

you can use `--help` to show options and help

# cvat module

## Small box

find the boxes with an area smaller than the image, for default tolerance is 1 (1% of area image)

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --in_file   | yes      | path to cvat xml file |
| --tolerance | no       | tolerance to filter   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python cvat smallbox --in_file <CVAT_XML> --tolerance <TOLERANCE>  > output.csv
```

## intersection box

find the boxes that intersect and are greater than the tolerance, for default tolerance is 70 (70% of the area of the small intersection box)

| COMMAND     | REQUIRED | DESCRIPTION           |
| ----------- | -------- | --------------------- |
| --in_file   | yes      | path to cvat xml file |
| --tolerance | no       | tolerance to filter   |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python cvat intersectionbox --in_file <CVAT_XML> --tolerance <TOLERANCE>  > output.csv
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

| COMMAND       | REQUIRED | DESCRIPTION                                                                                               |
| ------------- | -------- | --------------------------------------------------------------------------------------------------------- |
| --in_file     | yes      | path to geojson file                                                                                      |
| --id_label    | no       | name of key to id                                                                                         |
| --id_start    | no       | value of first id, the next value is its sequence (number)                                                |
| --zeros       | no       | add zeros at the beginning of the id, until it reaches the specified length. Example: --zeros 3 --> `003` |
| --variation   | no       | type of id (number or uuid), default=number                                                               |
| --output_file | yes      | Path to geojson output file                                                                               |

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:python  geo generateid --in_file <GEOJSON_PATH> --id_label <NEW_ID> --id_start 100 --zeros 5  --output_file S3://an-awesome-bucket-name/file.geojson
```
