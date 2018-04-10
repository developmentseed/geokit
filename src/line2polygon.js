const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function function_name(file) {
  var output = turf.featureCollection([]);
  var geojson = JSON.parse(fs.readFileSync(file).toString());
  geojson.features.forEach(function(line) {
    if (line.geometry.type === 'LineString') {
      var polygon = turf.lineToPolygon(line);
      polygon.properties = line.properties;
      output.features.push(polygon);
    }
  });

  console.log(JSON.stringify(output));
};
