# geokit

Command line tool for basic operations through geojson files!

## Install

```
git clone git@github.com:Rub21/geokit.git
cd geokit/
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
 geokit line2polygon input.geojson > output.geojson
 ```


### Set each feature into a row in files from Feature collection

```
 geokit fc2frows input.geojson > output.json
 ```

### Feature collection to CSV

This funcionality will add a `osm_download_link` column  in the csv.


```
geokit fc2csv polygons.geojson  > csv.csv
```

### Filter features by property

This funcionality will filter features by property and will generate a new geojson file with the filtered objects.

 ```
geokit filterbyprop <input.geojson> --prop building=* > output.geojson
 ```

### Count features by property

This funcionality will count features by property.

 ```
geokit countfeature <input.geojson> --prop building=* 
 ```
 ### Get area per each feature into the geojson file

This functionality will get the area of each feature (polygon) into a geojson file and will generate a new geojson file with all features with an area property.

 ```
geokit featurearea input.geojson > output.geojson  
 ```
 