const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function (file, unit, radius, prop) {
  const units = ['kilometers', 'miles', 'meters'];
  if (units.indexOf(unit) === -1) {
    console.log('Wrong unit, acceptable :' + units.join(', '));
  } else {
    const geojson = JSON.parse(fs.readFileSync(file).toString());
    let fc = turf.featureCollection([]);
    geojson.features.forEach(function (feature) {
      prop_value = 1
      if (prop && feature['properties'][prop])
        prop_value = feature['properties'][prop]
      prop_value = feature['properties'][prop] || 1
      let buffered = turf.buffer(feature, radius * prop_value, {
        units: unit
      });
      fc.features.push(buffered);
    });
    console.log(JSON.stringify(fc));
  }
};
