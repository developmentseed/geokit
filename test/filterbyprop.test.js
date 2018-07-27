const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdFilterbyprop = require('../src/filterbyprop.js');
const file = path.join(__dirname, '/fixtures/filterbyprop.geojson');
test('Filterbyprop', function (t) {
  logInterceptor();
  cmdFilterbyprop(file, 'building=*');
  let logs = logInterceptor.end();
  const fc = JSON.parse(logs[0]);
  let a = fc.features.length + fc.features.length;
  t.plan(a);
  for (let i = 0; i < fc.features.length; i++) {
    const propKey = fc.features[i].properties['building'];
    t.equal(propKey, 'yes', 'ok Propkey');
    const propType = fc.features[i].geometry.type;
    if (propType == 'Polygon') {
      t.equal(propType, 'Polygon', 'ok PropType');
    } else {
      t.equal(propType, 'MultiPolygon', 'ok PropType');
    }
  }
  t.end();
});

