const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function (file) {
  var geojson = JSON.parse(fs.readFileSync(file).toString());
  var bbox = turf.bbox(geojson);
  console.log(bbox)
};

