const fs = require('fs');
const turf = require('@turf/turf');
const JSONStream = require('JSONStream');
const eventStream = require('event-stream');
const cover = require('@mapbox/tile-cover');
const _ = require('underscore');

let collectionObj = {};
module.exports = function(file, zoom, buffer) {
  var fileStream = fs.createReadStream(file, {
    encoding: 'utf8'
  });
  fileStream
    .pipe(JSONStream.parse('features.*'))
    .pipe(
      eventStream.mapSync(function(data) {
        const tiles = buildTile(data, zoom, buffer);
        for (let d = 0; d < tiles.features.length; d++) {
          const tile = tiles.features[d];
          collectionObj[tile.properties.index] = tile;
        }
        return data;
      })
    )
    .on('error', function(error) {
      this.emit('end');
      console.log(error);
    })
    .on('close', function() {
      this.emit('end');
      const collection = turf.featureCollection(_.values(collectionObj));
      console.log(JSON.stringify(collection));
    });
};

function buildTile(data, zoom, buffer) {
  var limits = {
    min_zoom: zoom,
    max_zoom: zoom
  };
  var buffer_ = turf.buffer(data, buffer, { units: 'kilometers' });
  let polys = cover.geojson(buffer_.geometry, limits);
  const tiles = cover.tiles(buffer_.geometry, limits);
  const indexes = cover.indexes(buffer_.geometry, limits);
  for (let i = 0; i < polys.features.length; i++) {
    polys.features[i].properties.tiles = tiles[i];
    polys.features[i].properties.index = indexes[i];
  }
  return polys;
}
