#!/usr/bin/env node

const argv = require('minimist')(process.argv.slice(2));
const area = require('./src/area');
const bbox2fc = require('./src/bbox2fc');
const buffer = require('./src/buffer');
const clip = require('./src/clip');
const distance = require('./src/distance');
const line2polygon = require('./src/line2polygon');
const bbox = require('./src/bbox');

var action = argv._[0];
var file = argv._[1];
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
  default:
    console.log('unknown command');
}