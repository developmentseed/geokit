const fs = require('fs');
const readline = require('readline');
const geojson = {
  type: 'FeatureCollection',
  features: []
};

module.exports = function(file) {
  const rd = readline.createInterface({
    input: fs.createReadStream(file),
    output: process.stdout,
    terminal: false
  });
  rd.on('line', function(line) {
    const obj = JSON.parse(line);
    if (obj.type === 'FeatureCollection') {
      geojson.features = geojson.features.concat(obj.features);
    } else {
      geojson.features = geojson.features.concat(obj);
    }
  }).on('close', function() {
    process.stdout.write(JSON.stringify(geojson));
  });
};
