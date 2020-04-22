#!/usr/bin/env node
const argv = require('minimist')(process.argv.slice(2));
const path = require('path');
const exec = require('executive');
const fs = require('fs');
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
  case 'bbox':
    require('./src/bbox')(inputFile);
    break;
  case 'bbox2fc':
    require('./src/bbox2fc')(argv.bbox);
    break;
  case 'buffer':
    require('./src/buffer')(inputFile, argv.unit, argv.radius);
    break;
  case 'fc2square':
    require('./src/fc2square')(inputFile, argv.radius);
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
  case 'fc2frows':
    require('./src/fc2frows')(inputFile);
    break;
  case 'fc2csv':
    require('./src/fc2csv')(inputFile);
    break;
  case 'filterbyprop':
    require('./src/filterbyprop')(inputFile, argv.prop);
    break;
  case 'filterbygeometry':
    require('./src/filterbygeometry')(inputFile, argv.geos);
    break;
  case 'countfeature':
    require('./src/countfeature')(inputFile, argv.prop);
    break;
  case 'featurearea':
    require('./src/featurearea')(inputFile);
    break;
  case 'featuredistance':
    require('./src/featuredistance')(inputFile);
    break;
  case 'countbysize':
    require('./src/countbysize')(inputFile, argv.psize);
    break;
  case 'difference':
    require('./src/difference')(inputFile, argv._[2], argv.key);
    break;
  case 'duplicatefeatures':
    require('./src/duplicateFeatures')(inputFile, argv.key);
    break;
  case 'point2tile':
    require('./src/point2tile')(inputFile, argv.zoom, argv.buffer, argv.copyattrs);
    break;
  case 'tilecover':
    require('./src/tileCover')(inputFile, argv.zoom);
    break;
  case 'deletenulls':
    require('./src/deletenulls')(inputFile);
    break;
  case 'jsonlines2geojson':
    require('./src/jsonlines2geojson')(inputFile);
    break;
  case 'centroid':
    require('./src/centroid')(inputFile);
    break;
  case 'splitbyzoom':
    require('./src/splitbygrid')(inputFile, argv.folder, argv.zoom);
    break;
  case 'addattributefc':
    require('./src/addattributefc')(inputFile, argv.prop);
    break;
  case 'keepattributes':
    require('./src/keepattributes')(inputFile, argv.keys);
    break;
  case 'renamekey':
    require('./src/renamekey')(inputFile, argv.key);
    break;
  //Python scripts section
  case 'removeactionosm':
    scriptPath = path.join(__dirname, '/python-scripts/remove_acction_obj.py');
    cmd = ['python', scriptPath, inputFile, outputFile];
    exec(cmd.join(' '), outputFunction);
    break;
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
  case 'cvat-count-tags':
    scriptPath = path.join(__dirname, '/python-scripts/cvat-count-tags.py');
    cmd = ['python', scriptPath, inputFile, outputFile];
    exec(cmd.join(' '), outputFunction);
    break;
  case 'cvat-xml2csv':
    scriptPath = path.join(__dirname, '/python-scripts/cvat-xml2csv.py');
    cmd = ['python', scriptPath, argv.full ? '--full' : '', inputFile];
    exec(cmd.join(' '), outputFunction);
    break;
  case 'downsized-imgs':
    scriptPath = path.join(__dirname, '/python-scripts/downsized-imgs.py');
    cmd = ['python', scriptPath, inputFile];
    exec(cmd.join(' '), outputFunction);
    break;
  case 'cvat-npz2xml':
    scriptPath = path.join(__dirname, '/python-scripts/cvat-npz2xml.py');
    cmd = ['python', scriptPath, inputFile, argv.imgPath, argv.imgLabel];
    exec(cmd.join(' '), outputFunction);
    break;
  case 'cvat-xml2npz':
    scriptPath = path.join(__dirname, '/python-scripts/cvat-xml2npz.py');
    cmd = ['python', scriptPath, inputFile];
    exec(cmd.join(' '), outputFunction);
    break;
  //help
  case 'help':
  case '--help':
  default:
    console.log(fs.readFileSync(path.join(__dirname, '/cli.txt'), 'UTF-8'));
}

function outputFunction(error, stdout, stderr) {
  if (error) console.log(error);
  // console.log(stdout);
}
