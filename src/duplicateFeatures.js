const fs = require('fs');
const _ = require('underscore');
const turf = require('@turf/turf');
module.exports = function(file, key) {
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  let duplicates = {};
  geojson.features.map(feature => {
    if (duplicates[feature.properties[key]]) {
      duplicates[feature.properties[key]].push(feature.properties[key]);
    } else {
      duplicates[feature.properties[key]] = [feature.properties[key]];
    }
  });
  let duplicateFeatures = turf.featureCollection([]);

  _.each(duplicates, function(v, k) {
    if (v.length > 1) {
      duplicateFeatures.features = duplicateFeatures.features.concat(v);
    }
  });
  console.log(JSON.stringify(duplicateFeatures));
};
