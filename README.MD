# geokit

Command line tool for basic operations through geojson files!

## Install

```
git clone https://github.com/Rub21/geoarea.git
cd geoarea/
npm link

```

## Usage

#### Area

- Get the area polygon geojson file in KM2.

```
geokit area <input.geojson>

```


### Bbox to featurecollection

- Convert bbox to feature collection: bbox extent in minX, minY, maxX, maxY order

```
geokit bbox2fc --bbox="0, 0, 10, 10" > output.geojson

```


### Buffer

- Create buffer in lineStrings features.

```
geokit buffer  <input.geojson> --unit=meters --radius=10000  > output.geojson

```


### Clip

Clip geojson file.

```
geokit clip map.geojson boundaries.geojson > o.geojson
```



### Distance

Get distance of geojson file, applicable only for LineString, and MultiLineString

```
geokit distance imput.geojson

```


### Line 2 polygon

```
 geokit line2polygon input.geojson   > output.geojson
 ```

