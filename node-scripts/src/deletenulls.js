const fs = require('fs');
const turf = require('@turf/turf');
const _ = require('underscore');
module.exports = function(file) {
  const geojson = JSON.parse(fs.readFileSync(file).toString());

  for (var i = 0; i < geojson.features.length; i++) {
    _.each(geojson.features[i].properties, function(val, key) {
      if (!val && val !== 0) {
        delete geojson.features[i].properties[key];
      }
    });
  }
  console.log(JSON.stringify(geojson));
};
