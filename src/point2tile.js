const fs = require('fs');
const turf = require('@turf/turf');
const JSONStream = require('JSONStream');
const eventStream = require('event-stream');
const cover = require('@mapbox/tile-cover');
const _ = require('underscore');

let collectionObj = {};
module.exports = function(file, zoom) {
  var fileStream = fs.createReadStream(file, {
    encoding: 'utf8'
  });
  fileStream
    .pipe(JSONStream.parse('features.*'))
    .pipe(
      eventStream.mapSync(function(data) {
        const tile = buildTile(data, zoom);
        collectionObj[tile.properties.index] = tile;
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

function buildTile(data, zoom) {
  var limits = {
    min_zoom: zoom,
    max_zoom: zoom
  };
  let poly = cover.geojson(data.geometry, limits).features[0];
  const tiles = cover.tiles(data.geometry, limits);
  const indexes = cover.indexes(data.geometry, limits);
  poly.properties = {};
  poly.properties.tiles = tiles;
  poly.properties.index = indexes[0];
  return poly;
}
