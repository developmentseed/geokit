const fs = require('fs');
module.exports = function (file) {
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  for (let i = 0; i < geojson.features.length; i++) {
    const feature = geojson.features[i];
    console.log(JSON.stringify(feature));
  }
};
