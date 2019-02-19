const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdTileCover = require('../src/tileCover');
const file = path.join(__dirname, '/fixtures/polygon.geojson');
test('tile Cover', function(t) {
  t.plan(1);
  logInterceptor();
  cmdTileCover(file, 15, 0.2);
  let logs = logInterceptor.end();
  const fc = JSON.parse(logs[0]);
  t.equal(fc.features.length, 4, ' Size of features 4');
  t.end();
});
