const fs = require('fs');
const turf = require('@turf/turf');
module.exports = function (file) {
    const geojson = JSON.parse(fs.readFileSync(file).toString());
    const bbox = turf.bbox(geojson);
    //console.log(JSON.stringify(bbox));
    var cellSide = 5;
    var options = { units: 'kilometers' };

    var squareGrid = turf.squareGrid(bbox, cellSide, options);
    console.log(JSON.stringify(squareGrid));
};
