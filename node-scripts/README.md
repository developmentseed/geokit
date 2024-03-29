# Geokit-node

Geokit-node is a command-line interface (CLI) tool written in node. Geokit is installed with docker, due several functionalities from other repositories like [awesome-geojson](https://github.com/tmcw/awesome-geojson) were incorporated to Geokit functionalities.


- **Building from repo**
```
git clone git@github.com:developmentseed/geokit.git
cd geokit/
docker-compose build
alias geokit='docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:node.latest geokit'
```

- **Building from [docker-hub](https://hub.docker.com/r/developmentseed/geokit)**

```
alias geokit='docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:node.latest geokit'
```

# Install for development mode

```
docker-compose run geokit
```

or

```
cd geokit/
docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:node.latest bash
```

# Usage

### Area

- Gets the total area in km² of polygon features that there are in a geojson file.

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

- Creates features' buffer for a given radius.

```
geokit buffer input.geojson --unit=meters --radius=10000  > output.geojson
```

### Feature to square

- Creates features' square for a given radius in meters, in case of Polygon and LineString the script takes the centroid to generate the square

```
geokit fc2square input.geojson --radius=40  > output.geojson
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

### Add on each Feature

```
geokit addattributefc input.geojson --prop "type=hospital" > output.geojson
```

### Filter features by property

- Filters features by given property and it will generate a new geojson file with the filtered features.

```
geokit filterbyprop input.geojson --prop building=* > output.geojson
```

### Filter features by geometry

- Filters features by given one or many geometry types and it will generate a new geojson file with the filtered features.

*<geometry_types>:* Could be Polygon, LineString, etc.

```
geokit filterbygeometry input.geojson --geos <geometry_types> > ouput.geojson
```

### Count features by property

- Gets the total number of features that exist inside the a geojson file (according to a chosen property).

```
geokit countfeature input.geojson --prop building=* 
```

### Set area on each feature in a geojson file

- Gets the area in m² of each feature (polygon) into a geojson file and it will generate a new geojson file with all features plus an area property.

```
geokit featurearea input.geojson > output.geojson  
```

### Set bbox on each feature in a geojson file

```
geokit featurebbox input.geojson > output.geojson  
```

### Set distance in kilometers on each feature in a geojson file

```
geokit featuredistance input.geojson > output.geojson  
```

### Count features by area size

- Counts features larger than the given area size in km². Applicable for polygons.

```
geokit countbysize input.geojson --psize=1000
```

### Difference between two geojson files according to an attribute

- Gets the difference of the objects between two geojson files according to a common attribute.

*--key*: Could be any of attribute, which is in both files.

```
geokit difference <file1.geojson>  <file2.geojson> --key=school_code
```

### Keep attributes in feature

```
geokit keepattributes <file1.geojson>  --keys="id,power,timestamp" > output.geojson
```

### Rename key in properties

```
geokit renamekey <file1.geojson>  --key="idBuilding>id" > output.geojson
```

### Duplicate objects by an attribute

- Gets the duplicate objects, identified by a unique attribute or primary key.

```
geokit duplicatefeatures <file1.geojson> --key=id
```

### Features to tiles

- Pass a geojson with points and get the nearest tiles to this point in a geojson file.

```
geokit point2tile <file.geojson> --zoom=17 --buffer=0.2 --copyattrs=true > tiles.geojson
```

### Tile Cover

- Pass a polygon and get the tiles which cover all the polygon at a certain zoom.
From: https://github.com/mapbox/tile-cover

```
 geokit tilecover polygon.geojson --zoom=15 > tiles.geojson

```

### Delete nulls

- Deletes the attributes that have a null value.

```
 geokit deletenulls input.geojson > output.geojson

```

### JSON to GeoJSON

- Gets a geojson file from json file.

```
 geokit jsonlines2geojson input.json > output.geojson

```

### Feature to point 

- Gets the centroid for each features.

```
 geokit centroid input.geojson > output.geojson

```

### Split a file according to zoom level

- Divides the features into a geojson file according to a given zoom level (works for zoom <= 15), and it will generate geojson files into a folder.

```
 geokit splitbyzoom input.geojson --folder=foldername --zoom=10
```

## Other functionalities into a Docker image:

Functionalities outside Geokit into a Docker image.


### [osmtogeojson](https://github.com/tyrasd/osmtogeojson)

- Converts osm file to geojson format.

```
osmtogeojson input.osm > output.geojson
```

### [geojsontoosm](https://github.com/Rub21/geojson2osm)

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
