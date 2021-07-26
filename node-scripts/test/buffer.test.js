const test = require('tape');
const fs = require('fs');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdBuffer = require('../src/buffer.js');
const file = path.join(__dirname, '/fixtures/linestring.geojson');
const bufferGeojson = JSON.parse(fs.readFileSync(path.join(__dirname, '/fixtures/buffer.geojson')));
test('Buffer', function(t) {
  t.plan(2);
  logInterceptor();
  cmdBuffer(file, 'kilometers', 0.005);
  let logs = logInterceptor.end();
  const fc = JSON.parse(logs[0]);
  t.equal(fc.features[0].geometry.type, bufferGeojson.features[0].geometry.type, 'ok Polygon type');
  t.deepEqual(
    fc.features[0].geometry.coordinates[0][0],
    bufferGeojson.features[0].geometry.coordinates[0][0],
    'ok coordinates type'
  );
  t.end();
});
