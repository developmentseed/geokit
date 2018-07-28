const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdArea = require('../src/area.js');
const file = path.join(__dirname, '/fixtures/monaco.geojson');
test('Area', function(t) {
  t.plan(1);
  logInterceptor();
  cmdArea(file);
  let logs = logInterceptor.end();
  const area = parseFloat(logs[0]);
  t.equal(area, 2.35533, 'Monaco area 2.35533 km2');
  t.end();
});
