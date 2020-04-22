const fs = require('fs');
const JSONStream = require('JSONStream');
const eventStream = require('event-stream');
const turf = require('@turf/turf');
module.exports = function(file, keys) {
  const keepKeys = keys.toLowerCase().split('>');
  const fileStream = fs.createReadStream(file, {
    encoding: 'utf8'
  });
  let features = [];
  fileStream
    .pipe(JSONStream.parse('features.*'))
    .pipe(
      eventStream.mapSync(function(data) {
        data.properties[keepKeys[1]] = data.properties[keepKeys[0]];
        delete data.properties[keepKeys[0]];
        features.push(data);
        return data;
      })
    )
    .on('error', function(error) {
      this.emit('end');
      console.log(error);
    })
    .on('close', function() {
      process.stdout.write(JSON.stringify(turf.featureCollection(features)));
      this.emit('end');
    });
};
