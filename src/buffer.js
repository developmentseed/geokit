const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file, unit, radius) {
  const units = ['kilometers', 'miles', 'meters'];
  if (units.indexOf(unit) === -1) {
    console.log('Wrong unit, acceptable :' + units.join(', '));
  } else {
    const geojson = JSON.parse(fs.readFileSync(file).toString());
    let fc = turf.featureCollection([]);
    geojson.features.forEach(function(feature) {
      let buffered = turf.buffer(feature, radius, {
        units: unit
      });
      fc.features.push(buffered);
    });
    console.log(JSON.stringify(fc));
  }
};
