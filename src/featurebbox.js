const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file) {
  const obj = JSON.parse(fs.readFileSync(file).toString());
  for (let i = 0; i < obj.features.length; i++) {
    obj.features[i].properties.bbox = turf.bbox(obj.features[i]);
  }
  console.log(JSON.stringify(obj));
};
