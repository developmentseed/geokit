const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file) {
  let output = turf.featureCollection([]);
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  geojson.features.forEach(function(object) {
    if (object.geometry.type === 'Polygon' || object.geometry.type === 'MultiPolygon') {
      let point = turf.centroid(object);
      point.properties = object.properties;
      output.features.push(point);
    } else {
      output.features.push(object);
    }
  });
  console.log(JSON.stringify(output));
};
