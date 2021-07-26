const fs = require('fs');
const turf = require('@turf/turf');
const config = require('./../config');
const Json2csvParser = require('json2csv').Parser;
const _ = require('underscore');

module.exports = function(file) {
  const geojson = JSON.parse(fs.readFileSync(file).toString());
  let properties = [];
  let headers = [];
  for (let i = 0; i < geojson.features.length; i++) {
    const bbox = turf.bbox(geojson.features[i]);
    geojson.features[i].properties.osm_download_link = `${config.josmRemote}/load_and_zoom?left=${bbox[0]}&bottom=${
      bbox[1]
    }&right=${bbox[2]}&top=${bbox[3]}`;
    headers = _.unique([].concat(_.keys(geojson.features[i].properties)));
    properties.push(geojson.features[i].properties);
  }
  const json2csvParser = new Json2csvParser({ headers });
  const csv = json2csvParser.parse(properties);
  console.log(csv);
};
