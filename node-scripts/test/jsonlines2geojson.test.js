const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdJsonlines2geojson = require('../src/jsonlines2geojson.js');
const file = path.join(__dirname, '/fixtures/jsonlines2geojson.json');
test('jsonlines2geojson', function(t) {
  t.plan(1);
  logInterceptor();
  cmdJsonlines2geojson(file);
  setTimeout(function() {
    let logs = logInterceptor.end();
    const fc = JSON.parse(logs);
    t.equal(fc.features.length, 13, 'ok num of features');
    t.end();
  }, 200);
});
