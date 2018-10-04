const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file) {
  let output = turf.featureCollection([]);
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  geojson.features.forEach(function(object) {
    if (object.geometry.type === 'LineString') {
      let polygon = turf.lineToPolygon(object);
      polygon.properties = object.properties;
      output.features.push(polygon);
    }else{
      output.features.push(object);
    }
  });
  console.log(JSON.stringify(output));
};
