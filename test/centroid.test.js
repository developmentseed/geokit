const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdPoly2point = require('../src/centroid.js');
const file = path.join(__dirname, '/fixtures/poly2point.geojson');
test('centroid', function(t) {
  t.plan(1);
  logInterceptor();
  cmdPoly2point(file);
  let logs = logInterceptor.end();
  const fc = JSON.parse(logs[0]);
  t.equal(fc.features[0].geometry.type, 'Point', 'ok Point type');
  t.end();
});
