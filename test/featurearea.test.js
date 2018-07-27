const test = require('tape');
const fs = require('fs');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdAreaF = require('../src/featurearea.js');
const file = path.join(__dirname, '/fixtures/area.geojson');
const outputfile = JSON.parse(fs.readFileSync(path.join(__dirname, '/fixtures/output.geojson')));
test('AreaF', function (t) {
	t.plan(1);
	logInterceptor();
	cmdAreaF(file);
	let logs = logInterceptor.end();
	const fc = JSON.parse(logs[0]);
	t.deepEqual(fc, outputfile, 'Ok');
	t.end();
});