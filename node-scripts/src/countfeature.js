const fs = require('fs');
module.exports = function(file, prop) {
  let totfeature = 0;
  const propKey = prop.split('=')[0];
  const propValues = prop.split('=')[1].split(',');
  const geojson = JSON.parse(fs.readFileSync(file).toString());

  geojson.features.forEach(function(feature) {
    if (feature.properties) {
      let attr = feature.properties[propKey];
      if ((propValues[0] === '*' && feature.properties[propKey]) || propValues.indexOf(attr) > -1) {
        totfeature = totfeature + 1;
      }
    }
  });
  console.log(totfeature);
};
