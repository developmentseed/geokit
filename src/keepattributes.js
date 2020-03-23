const fs = require('fs');
const JSONStream = require('JSONStream');
const eventStream = require('event-stream');
const turf = require('@turf/turf');
module.exports = function (file, keys) {
  const keepKeys = keys.split(',');
  const fileStream = fs.createReadStream(file, {
    encoding: 'utf8'
  });
  let features = [];
  fileStream
    .pipe(JSONStream.parse('features.*'))
    .pipe(
      eventStream.mapSync(function (data) {
        let newProps = {};
        Object.keys(data.properties).forEach(key => {
          if (keepKeys.indexOf(key) > -1) {
            newProps[key] = data.properties[key];
          }
        });
        data.properties = newProps;
        features.push(data);
        return data;
      })
    )
    .on('error', function (error) {
      this.emit('end');
      console.log(error);
    })
    .on('close', function () {
      process.stdout.write(JSON.stringify(turf.featureCollection(features)));
      this.emit('end');
    });
};
