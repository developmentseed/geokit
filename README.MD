# Geokit

[![Build Status](https://travis-ci.org/developmentseed/geokit.svg?branch=master)](https://magnum.travis-ci.com/developmentseed/geokit)

Geokit is a command-line interface (CLI) tool written in javascript, that contains all the basic functionalities for measurements, conversions and operations of geojson files.

# Install Geokit CLI by Container

Geokit is installed with docker, due several functionalities from other repositories like [awesome-geojson](https://github.com/tmcw/awesome-geojson) were incorporated to Geokit functionalities.

Clone the repository and build the docker image, also you can use an alias to avoid write all the command to run the Docker image.

```
docker build -t geokit-container .
alias geokit='docker run --rm -v ${PWD}:/app geokit-container:latest geokit'
```

# Usage

### Area

- Gets the total area in km² of Polygon and MultiPolygon features that there are in a geojson file.

```
geokit area input.geojson
```

### Bbox of FeatureCollection

- Gets the bbox of a FeatureCollection.

```
geokit bbox input.geojson
```

### Bbox to FeatureCollection

- Converts a bbox to FeatureCollection. 

```
geokit bbox2fc --bbox="0, 0, 10, 10" > output.geojson
```

### Buffer

- Creates a buffer in LineString features for a given radius.

```
geokit buffer input.geojson --unit=meters --radius=10000  > output.geojson
```

### Clip

- Gets only the features that are inside the given boundary and it deletes all features outside the boundary.

```
geokit clip input.geojson boundary.geojson > output.geojson
```

### Distance

- Gets the total distance in km of LineString and MultiLineString features that there are in a geojson file.

```
geokit distance input.geojson
```

### Line to polygon

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

- Adds an osm_download_link column per each feature and each link downloads the feature in JOSM.

```
geokit fc2csv input.geojson > output.csv
```

### Filter features by property

- Filters features by given property and it will generate a new geojson file with the filtered features.

```
geokit filterbyprop input.geojson --prop building=* > output.geojson
```

### Filter features by geometry

- Filters features by given one or many geometry types and it will generate a new geojson file with the filtered features.

```
geokit filterbygeometry --geos <geometry types> > ouput.geojson
```

### Count features by property

- Gets the total number of features that exist inside the a geojson file (according to a chosen property).

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
geokit countbysize input.geojson --psize=1000   
```

## Other functionalities into a Docker image:

Functionalities outside Geokit into a Docker image.

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

- Converts geojson polygons to OpenStreetMap (OSM) poly format file.

```
geojson2poly input.geojson output.poly
```

### [geojson-pick](https://www.npmjs.com/package/geojson-pick)

- Removes all but specified properties from features in a geojson FeatureCollection.

```
geojson-pick PROPERTYNAME1 < input.geojson > output.geojson
```
