const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file, unit, radius) {
  var units = ['kilometers', 'miles', 'meters'];
  if (units.indexOf(unit) === -1) {
    console.log('Wrong unit, acceptable :' + units.join(', '));
  } else {
    var geojson = JSON.parse(fs.readFileSync(file).toString());
    var fc = turf.featureCollection([]);
    geojson.features.forEach(function(feature) {
      if (feature.geometry.type == 'LineString') {
        var buffered = turf.buffer(feature, radius, {
          units: unit
        });
        fc.features.push(buffered);
      }
    });
    console.log(JSON.stringify(fc));
  }
};
