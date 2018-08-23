const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file, prop, psize) {
  let totfeature = 0;
  const propKey = prop.split('=')[0];
  const propValues = prop.split('=')[1].split(',');
  const geojson = JSON.parse(fs.readFileSync(file).toString());

  geojson.features.forEach(function(feature) {
    if (feature.properties) {
      let attr = feature.properties[propKey];
      if ((propValues[0] === '*' && feature.properties[propKey]) || propValues.indexOf(attr) > -1 && feature.geometry.type === 'Polygon') {
        let area = turf.area(feature);
        let areaha = (area / 10000).toFixed(0);
        if (areaha > psize) {
          totfeature = totfeature + 1;
        }
      }
    }
  });
  console.log(totfeature);
};