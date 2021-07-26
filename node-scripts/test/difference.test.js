const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdDifference = require('../src/difference');
const file1 = path.join(__dirname, '/fixtures/point-difference1.geojson');
const file2 = path.join(__dirname, '/fixtures/point-difference2.geojson');

test('Difference', function(t) {
  t.plan(1);
  logInterceptor();
  cmdDifference(file1, file2, 'id');
  setTimeout(function() {
    let logs = logInterceptor.end();
    const fc = JSON.parse(logs[0]);
    t.equal(fc.features[0].properties.id, '456', 'ok diffenrence');
    t.end();
  }, 300);
});
