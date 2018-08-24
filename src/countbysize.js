const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file, psize) {
  let totfeature = 0;
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  geojson.features.forEach(function(feature) {
    let area = turf.area(feature);
    let areaha = (area / 10000).toFixed(0);
    if (areaha > psize) {
      totfeature = totfeature + 1;
    }
  });
  console.log(totfeature);
};
