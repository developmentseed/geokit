const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file) {
  const obj = JSON.parse(fs.readFileSync(file).toString());
  for (let i = 0; i < obj.features.length; i++) {
    let areafeature = turf.area(obj.features[i]);
    areafeatureha = (areafeature / 1000000 * 100).toFixed(0);
    obj.features[i].properties.area = areafeatureha + 'ha';
  }
  console.log(JSON.stringify(obj));
};
