const fs = require('fs');
const turf = require('@turf/turf');
const JSONStream = require('JSONStream');
const eventStream = require('event-stream');

module.exports = function(file, radius) {
  let fc = turf.featureCollection([]);
  const fileStream = fs.createReadStream(file, {
    encoding: 'utf8'
  });
  fileStream
    .pipe(JSONStream.parse('features.*'))
    .pipe(
      eventStream.mapSync(function(feature) {
        const centroid = turf.centroid(feature);
        const bufer = turf.buffer(centroid, radius, {
          units: 'meters'
        });
        const polygon = turf.bboxPolygon(turf.bbox(bufer));
        polygon.properties = feature.properties;
        fc.features.push(polygon);
        return polygon;
      })
    )
    .on('error', function(error) {
      this.emit('end');
      console.log(error);
    })
    .on('close', function() {
      this.emit('end');
      console.log(JSON.stringify(fc));
    });
};
