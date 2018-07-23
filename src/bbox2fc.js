const turf = require('@turf/turf');
module.exports = function(bbox) {
  bbox = bbox.split(',').map(function(item) {
    return parseFloat(item);
  });
  const poly = turf.bboxPolygon(bbox);
  console.log(JSON.stringify(turf.featureCollection([poly])));
};
