const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file, polygonSize) {
  let totalFeature = 0;
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  geojson.features.forEach(function(feature) {
    let area = turf.area(feature);
    let areaha = (area / 10000).toFixed(0);
    if (areaha >= polygonSize) {
      totalFeature = totalFeature + 1;
    }
  });
  console.log(totalFeature);
};
