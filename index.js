#!/usr/bin/env node
const argv = require('minimist')(process.argv.slice(2));
const path = require('path');
const exec = require('executive');
const action = argv._[0];
const inputFile = argv._[1];
const outputFile = argv._[2];
let scriptPath;
let cmd;

switch (action) {
  //Node Apps
  case 'area':
    require('./src/area')(inputFile);
    break;
  case 'bbox2fc':
    require('./src/bbox2fc')(argv.bbox);
    break;
  case 'buffer':
    require('./src/buffer')(inputFile, argv.unit, argv.radius);
    break;
  case 'clip':
    require('./src/clip')(inputFile, argv._[2]);
    break;
  case 'distance':
    require('./src/distance')(inputFile);
    break;
  case 'line2polygon':
    require('./src/line2polygon')(inputFile);
    break;
  case 'bbox':
    require('./src/bbox')(inputFile);
    break;
  case 'fc2frows':
    require('./src/fc2frows')(inputFile);
    break;
  case 'fc2csv':
    require('./src/fc2csv')(inputFile);
    break;
  case 'filterbyprop':
    require('./src/filterbyprop')(inputFile, argv.prop);
    break;
  case 'countfeature':
    require('./src/countfeature')(inputFile, argv.prop);
    break;
  case 'featurearea':
    require('./src/featurearea')(inputFile);
    break;
  case 'countbysize':
    require('./src/countbysize')(inputFile, argv.psize);
    break;
  case 'filterbygeometry':
    require('./src/filterbygeometry')(inputFile, argv.geos);
    break;
  //Python scripts section
  case 'osm2new':
    scriptPath = path.join(__dirname, '/python-scripts/osm2new.py');
    cmd = ['python', scriptPath, inputFile, outputFile];
    exec(cmd.join(' '), outputFunction);
    break;
  case 'fixordinal':
    scriptPath = path.join(__dirname, '/python-scripts/fix_ordinal_suffixes.py');
    cmd = ['python', scriptPath, inputFile, outputFile];
    exec(cmd.join(' '), outputFunction);
    break;
  //help  
  case 'help':
    usage();
    break;
  case '--help':
    usage();
    break;
  default:
    usage();  
}

function outputFunction(error, stdout, stderr) {
  if(error) console.log(error);
  console.log(stdout);
};

function usage() {
  console.log('Commands:');
    console.log('  area             Gets the total area in km2 of the all polygons that there are in a geojson file');
    console.log('  bbox             Gets the bbox of a geojson file');
    console.log('  bbox2fc          Converts a bbox to FeatureCollection');
    console.log('  buffer           Creates buffer in LineString features for a given radius');
    console.log('  clip             Gets only the features that are inside the given boundary and it deletes all features outside the boundary');
    console.log('  distance         Gets the total distance in km of LineString and MultiLineString features that there are in a geojson file');
    console.log('  line2polygon     Changes the type of geometry from LineString to Polygon');
    console.log('  fc2frows         Sets each feature into a row from FeatureCollection');
    console.log('  fc2csv           Adds an osm_download_link column per each feature and each link downloads the feature in JOSM');
    console.log('  filterbyprop     Filters features by given property');
    console.log('  filterbygeometry Filters features by given one or many geometry types');
    console.log('  countfeature     Gets the total number of features that exist inside the a geojson file');
    console.log('  featurearea      Gets the area in hectares of each feature (polygon) into a geojson file');
    console.log('  countbysize      Counts features larger than the given area size in hectares');
    console.log('Also you can use these commands:');
    console.log('  geojson-merge    Merges multiple geojson files into one FeatureCollection');
    console.log('  osmtogeojson     Converts osm file to geojson format');
    console.log('  geojsontoosm     Converts geojson file to osm format');
    console.log('  geojson2poly     Converts geojson polygons to OpenStreetMap (OSM) poly format file');
    console.log('  geojson-pick     Removes all but specified properties from features in a geojson FeatureCollection');
    console.log('More details, visit our web page with all documentation --> http://devseed.com/geokit-doc-seed/')
}
