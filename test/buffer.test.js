const test = require('tape');
const fs = require('fs');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdBuffer = require('../src/buffer.js');
const file = path.join(__dirname, '/fixtures/linestring.geojson');
const bufferGeojson = JSON.parse(fs.readFileSync(path.join(__dirname, '/fixtures/buffer.geojson')));
test('Buffer', function (t) {
  t.plan(1);
  logInterceptor();
  cmdBuffer(file, 'kilometers', 0.005);
  let logs = logInterceptor.end();
  const fc = JSON.parse(logs[0]);
  t.deepEqual(fc, bufferGeojson, 'ok FeatureCollection');
  t.end();
});