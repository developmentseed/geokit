# geokit

[![Build Status](https://travis-ci.org/developmentseed/geokit.svg?branch=master)](https://magnum.travis-ci.com/developmentseed/geokit)

Command line tool for basic operations through geojson files!

# Install geokit CLI by Container (Recommended)

```
docker build -t geokit-container .
alias geokit='docker run --rm -v ${PWD}:/app geokit-container:latest geokit'
```

# Usage

### Area

- Gets the total area in km2 of the all polygons that there are in a geojson file.

```
geokit area input.geojson

```

### Bbox of a geojson

- Gets the bbox of a geojson file.

```
geokit bbox input.geojson
```


### Bbox to FeatureCollection

- Converts bbox to FeatureCollection: bbox extent in minX, minY, maxX, maxY order

```
geokit bbox2fc --bbox="0, 0, 10, 10" > output.geojson
```


### Buffer

- Creates buffer in LineString features.

```
geokit buffer  input.geojson --unit=meters --radius=10000 > output.geojson

```


### Clip

- Clips geojson file.

```
geokit clip input.geojson boundary.geojson > output.geojson
```


### Distance

- Gets the total distance in km of LineString and MultiLineString features that there are in a geojson file.

```
geokit distance input.geojson

```


### Line 2 polygon

- Changes the type of geometry from LineString to Polygon.

```
geokit line2polygon input.geojson > output.geojson
```


### Set each feature into a row 

- Sets each feature into a row from FeatureCollection.

```
geokit fc2frows input.geojson > output.json
```

### FeatureCollection to CSV

- Adds an osm_download_link column per each feature and will generate a csv file.

```
geokit fc2csv input.geojson  > output.csv
```

### Filter features by property

- Filters features by property and will generate a new geojson file with the filtered objects.

```
geokit filterbyprop input.geojson --prop building=* > output.geojson
```

### Count features by property

- Counts features into a geojson file by property.

```
geokit countfeature input.geojson --prop building=* 
```

### Get area per each feature into the geojson file

- Gets the area in hectares of each feature (polygon) into a geojson file and it will generate a new geojson file with all features plus an area property.

```
geokit featurearea input.geojson > output.geojson  
```

### Count features by area size

- Counts features larger than the given area size in hectares. Applicable for polygons.

```
geokit countbysize <input.geojson> --psize=1000   
```

## Other functionalities into a container:

### [geojson-merge](https://github.com/mapbox/geojson-merge)

- Merges multiple geojson files into one FeatureCollection.
```
geojson-merge input1.geojson input2.geojson > output.geojson
```

### [osmtogeojson](https://github.com/tyrasd/osmtogeojson)

- Converts osm file to geojson format.

```
osmtogeojson input.osm > output.geojson
```

### [geojsontoosm](https://github.com/tyrasd/geojsontoosm)

- Converts geojson file to osm format.

```
geojsontoosm input.geojson > output.osm
```

### [geojson2poly](https://www.npmjs.com/package/geojson2poly)

- Converts geojson polygons to openstreetmap (osm) poly format file.

```
geojson2poly input.geojson output.poly
```

### [geojson-pick](https://www.npmjs.com/package/geojson-pick)

- Removes all but specified properties from features in a geojson FeatureCollection.

```
geojson-pick PROPERTYNAME1 < input.geojson > output.geojson
```
