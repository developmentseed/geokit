const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdCount = require('../src/countbysize.js');
const file = path.join(__dirname, '/fixtures/f_size.geojson');
test('Countbysize', function(t) {
  t.plan(1);
  logInterceptor();
  cmdCount(file, 10);
  let logs = logInterceptor.end();
  const count = parseFloat(logs[0]);
  t.equal(count, 3, 'Ok total farmland larger than 10 is 3');
  t.end();
});
