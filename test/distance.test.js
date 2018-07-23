const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmd = require('../index.js');
const file = path.join(__dirname, '/fixtures/linestring.geojson');
test('Distance', function (t) {
  t.plan(1);
  logInterceptor();
  cmd.distance(file);
  let logs = logInterceptor.end();
  const distance = parseFloat(logs[0]);
  t.equal(distance, 2.25155, 'distance 2.25155 km');
  t.end();
});