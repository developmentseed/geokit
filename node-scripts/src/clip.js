const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function(file, clipFile) {
  //need stream reader here
  var geojson = JSON.parse(fs.readFileSync(file).toString());
  var clipmask = JSON.parse(fs.readFileSync(clipFile).toString());
  var fc = turf.featureCollection([]);
  clipmask.features.forEach(function(feature) {
    var bbox = turf.bbox(feature);
    geojson.features.forEach(function(f) {
      if (f.geometry.type === 'Point' || f.geometry.type === 'MultiPoint') {
        if (turf.booleanPointInPolygon(f, feature)) {
          fc.features.push(f);
        }
      } else {
        var clipped = turf.bboxClip(f, bbox);
        fc.features.push(clipped);
      }
    });
  });
  fc.features = fc.features.filter(function(item) {
    return item.geometry.coordinates.length > 0;
  });
  console.log(JSON.stringify(fc));
};
