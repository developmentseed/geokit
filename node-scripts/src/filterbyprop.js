const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file, prop) {
  let fcFilter = {};
  const propKey = prop.split('=')[0];
  const propValues = prop.split('=')[1].split(',');
  const geojson = JSON.parse(fs.readFileSync(file).toString());

  geojson.features.forEach(function(feature) {
    if (feature.properties) {
      let attr = feature.properties[propKey];
      if (
        (propValues[0] === '*' && feature.properties[propKey]) ||
        propValues.indexOf(attr) > -1 ||
        (!attr && propValues[0] == 'null')
      ) {
        if (fcFilter[propKey]) {
          fcFilter[propKey].push(feature);
        } else {
          fcFilter[propKey] = [feature];
        }
      }
    }
  });

  let features = [];
  if (fcFilter[propKey]) {
    features = fcFilter[propKey];
  }
  let fc = turf.featureCollection(features);
  console.log(JSON.stringify(fc));
};
