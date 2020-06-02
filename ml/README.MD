# Geokit-ml


Geokit-ml is a command-line interface (CLI) tool written in python3, that contains all the basic functionalities for measurements, conversions and operations of geojson files.


# Usage
### tips
you can use `--help` to show options and help

## Small box
find the boxes with an area smaller than the image, for default tolerance is 1 (1% of area image)

|COMMAND|ALIAS|REQUIRED|DESCRIPTION|
|---|---|--|---|
|input file|-i|yes|path to cvat xml file|
|tolerance|-t|no|tolerance to filter|

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit-ml:latest cvat_smallbox -i <CVAT_XML> -t <TOLERANCE>  > output.csv
```

## intersection box

find the boxes that intersect and are greater than the tolerance, for default tolerance is 70 (70% of the area of the small intersection box)

|COMMAND|ALIAS|REQUIRED|DESCRIPTION|
|---|---|--|---|
|input file|-i|yes|path to cvat xml file|
|tolerance|-t|no|tolerance to filter|

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit-ml:latest cvat_intersectionbox -i <CVAT_XML> -t <TOLERANCE>  > output.csv
``` 

## schools point

find school in [international schools database](https://www.international-schools-database.com)  and get point if exist. 

|COMMAND|ALIAS|REQUIRED|DESCRIPTION|
|---|---|--|---|
|city|-c|yes|name of city|

```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit-ml:latest rl_schoolspoint -c <CITY_NAME> > output.geojson
``` 

## geo generate id

Addig a key  `<id_label>` in the `PROPERTIES` in a geojson file, the value of `id` can start in `1` or `,start_count.`.

|COMMAND|ALIAS|REQUIRED|DESCRIPTION|
|---|---|--|---|
|input file|-i|yes|path to geojson file|
|label id|-l|no|name of key to id|
|start count|-s|no|value of first id, the next value is its sequence|
|zeros|-z|no|adds zeros at the beginning of the id, until it reaches the specified length. Example: -z 3   --> `003`|


```
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit-ml:latest geo_generateid -i <GEOJSON_PATH> -l new_id -s 100 -z 5 > output.geojson
``` 