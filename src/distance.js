const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file) {
  var distance = 0;
  var geojson = JSON.parse(fs.readFileSync(file).toString());
  if (geojson.features) {
    geojson.features.forEach(function(feature) {
      if (feature.geometry.type === 'LineString') {
        distance += SegmentDistance(feature);
      } else if (feature.geometry.type === 'MultiLineString') {
        for (var i = 0; i < feature.geometry.coordinates.length; i++) {
          var line = turf.lineString(feature.geometry.coordinates[i]);
          distance += SegmentDistance(line);
        }
      }
    });
    console.log(distance + ' MK');
  } else {
    console.log('Check if the geojson file is valid');
  }
};

function SegmentDistance(line) {
  var lineDistance = 0;
  for (var i = 0; i < line.geometry.coordinates.length - 1; i++) {
    var coord1 = line.geometry.coordinates[i];
    var coord2 = line.geometry.coordinates[i + 1];
    var from = turf.point(coord1);
    var to = turf.point(coord2);
    var d = turf.distance(from, to, {
      units: 'kilometers'
    });
    lineDistance += d;
  }
  return lineDistance;
}
