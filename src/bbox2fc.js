const fs = require('fs')
const turf = require('@turf/turf');
module.exports = function(bbox) {
	bbox = bbox.split(',').map(function(item) {
		return parseInt(item, 10);
	});
	var poly = turf.bboxPolygon(bbox);
	console.log(JSON.stringify(turf.featureCollection([poly])));
}