const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdDuplicateFeatures = require('../src/duplicateFeatures');
const file1 = path.join(__dirname, '/fixtures/point-duplicateFeatures.geojson');

test('Duplicate', function(t) {
  t.plan(1);
  logInterceptor();
  cmdDuplicateFeatures(file1, 'id');
  setTimeout(function() {
    let logs = logInterceptor.end();

    const fc = JSON.parse(logs[0]);
    console.log(logs[0]);
    t.equal(fc.features.length, 2, 'ok duplicate');
    t.end();
  }, 300);
});
