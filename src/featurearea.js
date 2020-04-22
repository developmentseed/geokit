const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file) {
  const obj = JSON.parse(fs.readFileSync(file).toString());
  for (let i = 0; i < obj.features.length; i++) {
    let areafeature = Number(turf.area(obj.features[i]).toFixed(3));
    obj.features[i].properties.area = areafeature;
  }
  console.log(JSON.stringify(obj));
};
