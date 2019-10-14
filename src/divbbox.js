const turf = require('@turf/turf');
module.exports = function (bbox) {
  bbox = bbox.split(',').map(function (item) {
    return parseFloat(item);
  });

  var cellSide = 10;
  var options = { units: 'kilometers' };

  var squareGrid = turf.squareGrid(bbox, cellSide, options);
  console.log(JSON.stringify(squareGrid));
};
