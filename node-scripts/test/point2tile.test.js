const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdPoint2tile = require('../src/point2tile');
const file = path.join(__dirname, '/fixtures/point.geojson');
test('Point2tile', function(t) {
  t.plan(1);
  logInterceptor();
  cmdPoint2tile(file, 17, 0.2);
  setTimeout(function() {
    let logs = logInterceptor.end();
    const fc = JSON.parse(logs[0]);
    t.equal(fc.features[0].geometry.type, 'Polygon', 'ok Polygon type');
    t.end();
  }, 300);
});
