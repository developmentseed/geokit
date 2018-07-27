const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdLine2polygon = require('../src/line2polygon.js');
const file = path.join(__dirname, '/fixtures/line2polygon.geojson');
test('Line2polygon', function (t) {
  t.plan(1);
  logInterceptor();
  cmdLine2polygon(file);
  let logs = logInterceptor.end();
  const fc = JSON.parse(logs[0]);
  t.equal(fc.features[0].geometry.type, 'Polygon', 'ok Polygon type');  
  t.end();
});