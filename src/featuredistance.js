const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function (file) {
  const obj = JSON.parse(fs.readFileSync(file).toString());
  for (let i = 0; i < obj.features.length; i++) {
    if (obj.features[i].geometry.type === 'LineString') {
      obj.features[i].properties.distance = SegmentDistance(obj.features[i]);
    }
  }
  console.log(JSON.stringify(obj));
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
