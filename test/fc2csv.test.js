const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const fs = require('fs');
const fc2csv = require('../src/fc2csv.js');
const GEOJSONfile = path.join(__dirname, '/fixtures/fc2csv.geojson');
const CSVfile = path.join(__dirname, '/fixtures/expected.csv');
var f = fs.readFileSync(CSVfile, {
	encoding: 'utf-8'
}, function(err) {
	console.log(err);
});
var expected = f.split('\n');
test('fc2csv', function(t) {
	t.plan(2);
	logInterceptor();
	fc2csv(GEOJSONfile);
	let logs = logInterceptor.end();
	var result = logs[0].split('\n');
	t.equal(result[0], expected[0], ' the headers are equal');
	t.equal(result[1], expected[1], ' the bodies  are equal');
	t.end();
});
