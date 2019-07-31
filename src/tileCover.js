const fs = require('fs');
const turf = require('@turf/turf');
const cover = require('@mapbox/tile-cover');

module.exports = function(file, zoom) {
  var poly = JSON.parse(fs.readFileSync(file));
  var limits = {
    min_zoom: zoom,
    max_zoom: zoom
  };
  const geojson = cover.geojson(poly.features[0].geometry, limits);
  const tiles = cover.tiles(poly.features[0].geometry, limits);
  const indexes = cover.indexes(poly.features[0].geometry, limits);
  for (let i = 0; i < geojson.features.length; i++) {
    // Updating the id in order to support the https://github.com/developmentseed/chips-ahoy input
    geojson.features[i].id = `(${tiles[i].join(',')})`;
    geojson.features[i].properties.serial = i;
    geojson.features[i].properties.tiles = tiles[i];
    geojson.features[i].properties.index = indexes[i];
  }
  console.log(JSON.stringify(geojson));
};
