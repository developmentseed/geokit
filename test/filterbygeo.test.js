const test = require('tape');
const fs = require('fs');
const logInterceptor = require('log-interceptor');
const path = require('path');
const geofilter = require('../src/filterbygeo.js');
const file = path.join(__dirname, '/fixtures/geofilter.geojson');
const outputfilter = JSON.parse(fs.readFileSync(path.join(__dirname, '/fixtures/outputpolygon.geojson')));
test('geoFilter', function(t) {
	t.plan(2);
	logInterceptor();
	geofilter(file, 'type=Polygon');
	let logs = logInterceptor.end();
	const fc = JSON.parse(logs[0]);
	t.deepEqual(fc, outputfilter, 'Ok');
	t.equal(fc.features[0].geometry.type,outputfilter.features[0].geometry.type, 'Polygon Ok');
	t.end();
});