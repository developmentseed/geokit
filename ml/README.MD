# Geokit-ml


Geokit-ml is a command-line interface (CLI) tool written in python3, that contains all the basic functionalities for measurements, conversions and operations of geojson files.


# Usage
### tips
you can use `--help` to show options and help

## Small box
find the boxes with an area smaller than the image, for default tolerance is 1 (1% of area image)

|COMMAND|ALIAS|DESCRIPTION|
|---|---|---|
|input file|-i|path to cvat xml file|
|tolerance|-t|tolerance to filter|

```
 docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit-ml:latest geokit cvat_smallbox -i <CVAT_XML> -t <TOLERANCE>  > output.csv
```

## intersection box

find the boxes that intersect and are greater than the tolerance, for default tolerance is 70 (70% of the area of the small intersection box)

|COMMAND|ALIAS|DESCRIPTION|
|---|---|---|
|input file|-i|path to cvat xml file|
|tolerance|-t|tolerance to filter|

```
 docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit-ml:latest geokit cvat_intersectionbox -i <CVAT_XML> -t <TOLERANCE>  > output.csv
``` 
