const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file, type) {
  let fcFilter = {};
  const propKey = type.split('=')[0];
  const propValues = type.split('=')[1].split(',');
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  geojson.features.forEach(function(feature) {
    if (feature.geometry.type) {
      let attr = feature.geometry[propKey];
      if ((propValues[0] === '*' && feature.geometry[propKey]) || propValues.indexOf(attr) > -1) {
        if (fcFilter[propKey]) {
          fcFilter[propKey].push(feature);
        } else {
          fcFilter[propKey] = [feature];
        }
      }
    }
  });
  let fc = turf.featureCollection(fcFilter[propKey]);
  console.log(JSON.stringify(fc));
};
