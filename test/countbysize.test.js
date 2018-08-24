const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdCount = require('../src/countbysize.js');
const file = path.join(__dirname, '/fixtures/f_size.geojson');
test('Countbysize', function(t) {
	t.plan(1);
	logInterceptor();
	cmdCount(file, 8800);
	let logs = logInterceptor.end();
	const count = parseFloat(logs[0]);
	t.equal(count, 2, 'Ok total farmland larger than 8800 is 2');
	t.end();
});
