const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function (file) {
  let distance = 0;
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  if (geojson.features) {
    geojson.features.forEach(function (feature) {
      if (feature.geometry.type === 'LineString') {
        distance += SegmentDistance(feature);
      } else if (feature.geometry.type === 'MultiLineString') {
        for (let i = 0; i < feature.geometry.coordinates.length; i++) {
          const line = turf.lineString(feature.geometry.coordinates[i]);
          distance += SegmentDistance(line);
        }
      }
    });
    console.log(distance.toFixed(5));
  } else {
    console.log(0);
  }
};

function SegmentDistance(line) {
  let lineDistance = 0;
  for (let i = 0; i < line.geometry.coordinates.length - 1; i++) {
    const coord1 = line.geometry.coordinates[i];
    const coord2 = line.geometry.coordinates[i + 1];
    const from = turf.point(coord1);
    const to = turf.point(coord2);
    const d = turf.distance(from, to, {
      units: 'kilometers'
    });
    lineDistance += d;
  }
  return lineDistance;
}
