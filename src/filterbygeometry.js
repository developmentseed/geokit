const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function (file, geos) {
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  let result = turf.featureCollection([]);
  const geometries = geos.split(',');
  geojson.features.forEach(function (feature) {
    if (geometries.indexOf(feature.geometry.type) > -1) {
      result.features.push(feature);
    }
  });
  console.log(JSON.stringify(result));
};
