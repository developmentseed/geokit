const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file, gtype) {
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  let fc = turf.featureCollection([]);
  geojson.features.forEach(function(feature) {
    if (feature.geometry.type == gtype) {
      fc.features.push(feature);
    }
  });
  console.log(JSON.stringify(fc));
};
