#!/usr/bin/env node
const argv = require('minimist')(process.argv.slice(2));
const area = require('./src/area');
const bbox2fc = require('./src/bbox2fc');
const buffer = require('./src/buffer');
const clip = require('./src/clip');
const distance = require('./src/distance');
const line2polygon = require('./src/line2polygon');
const bbox = require('./src/bbox');
const fc2frows = require('./src/fc2frows');
const fc2csv = require('./src/fc2csv');
const action = argv._[0];
const file = argv._[1];

switch (action) {
  case 'area':
    area(file);
    break;
  case 'bbox2fc':
    bbox2fc(argv.bbox);
    break;
  case 'buffer':
    buffer(file, argv.unit, argv.radius);
    break;
  case 'clip':
    clip(file, argv._[2]);
    break;
  case 'distance':
    distance(file);
    break;
  case 'line2polygon':
    line2polygon(file);
    break;
  case 'bbox':
    bbox(file);
    break;
  case 'fc2frows':
    fc2frows(file);
    break;
  case 'fc2csv':
    fc2csv(file);
    break;
  default:
    console.log('unknown command');
}

module.exports={
  area,
  distance
}
