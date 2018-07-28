const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdCount = require('../src/countfeature.js');
const file = path.join(__dirname, '/fixtures/count.geojson');
test('Count', function(t) {
  t.plan(1);
  logInterceptor();
  cmdCount(file, 'building=*');
  let logs = logInterceptor.end();
  const count = parseFloat(logs[0]);
  t.equal(count, 28, 'Ok total building 28');
  t.end();
});
