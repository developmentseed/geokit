const fs = require('fs');
const JSONStream = require('JSONStream');
const eventStream = require('event-stream');
const turf = require('@turf/turf');
module.exports = function(file, keys) {
  const keepKeys = keys.toLowerCase().split(',');
  const fileStream = fs.createReadStream(file, {
    encoding: 'utf8'
  });
  let features = [];
  fileStream
    .pipe(JSONStream.parse('features.*'))
    .pipe(
      eventStream.mapSync(function(data) {
        let newProps = {};
        Object.keys(data.properties).forEach(key => {
          const key_ = key.toLowerCase();
          if (keepKeys.indexOf(key_) > -1) {
            newProps[key] = data.properties[key];
          }
        });
        data.properties = newProps;
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
