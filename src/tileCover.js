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
    geojson.features[i].properties.id = i;
    geojson.features[i].properties.tiles = tiles[i];
    geojson.features[i].properties.index = indexes[i];
  }
  console.log(JSON.stringify(geojson));
};
