const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function (file) {
  let area = 0;
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  geojson.features.forEach(function (feature) {
    area += turf.area(feature)
  });
  console.log((area/1000000).toFixed(5));
}