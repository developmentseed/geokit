const test = require('tape');
const fs = require('fs');
const logInterceptor = require('log-interceptor');
const path = require('path');
const clip = require('../src/clip.js');
const file = path.join(__dirname, '/fixtures/count.geojson');
const bound = path.join(__dirname,'/fixtures/boundary.geojson');
const outputclip = JSON.parse(fs.readFileSync(path.join(__dirname, '/fixtures/clip.geojson')));
test('Clip', function(t) {
	t.plan(1);
	logInterceptor();
	clip(file, bound);
	let logs = logInterceptor.end();
	const fc = JSON.parse(logs[0]);
	t.deepEqual(fc, outputclip, 'Ok');
	t.end();
});