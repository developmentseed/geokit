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
  default:
    console.log('unknown command, visit: https://developmentseed/github.io/geokit-doc-seed');
}

function outputFunction(error, stdout, stderr) {
  if(error) console.log(error);
  console.log(stdout);
}