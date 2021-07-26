const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file) {
  let output = turf.featureCollection([]);
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  geojson.features.forEach(function(object) {
    let point = turf.centroid(object);
    point.properties = object.properties;
    output.features.push(point);
  });
  console.log(JSON.stringify(output));
};
