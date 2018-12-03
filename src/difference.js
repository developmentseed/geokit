const fs = require('fs');
module.exports = function(file, difFile, key) {
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  const difObjects = JSON.parse(fs.readFileSync(difFile).toString());
  let featureObj = {};
  difObjects.features.forEach(function(feature) {
    featureObj[feature.properties[key]] = true;
  });
  geojson.features = geojson.features.filter(function(feature) {
    return !featureObj[feature.properties[key]];
  });
  console.log(JSON.stringify(geojson));
};
