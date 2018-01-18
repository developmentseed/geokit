#!/usr/bin/env node

const fs = require('fs')
const argv = require('minimist')(process.argv.slice(2));
const turf = require('@turf/turf');
const geojson = JSON.parse(fs.readFileSync(argv._[0]).toString());
var area = 0;
geojson.features.forEach(function(feature) {
	area += turf.area(feature) / 1000000;
})
console.log(area + ' MK2');