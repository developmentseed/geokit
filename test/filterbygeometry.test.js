const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmdFilterbygeo = require('../src/filterbygeometry.js');
const file = path.join(__dirname, '/fixtures/filterbygeo.geojson');
test('Filterbygeo', function(t) {
  logInterceptor();
  cmdFilterbygeo(file, 'Polygon');
  let logs = logInterceptor.end();
  const fc = JSON.parse(logs[0]);
  let a = fc.features.length;
  t.plan(a);
  for (let i = 0; i < fc.features.length; i++) {
    const gtype = fc.features[i].geometry.type;
    if (gtype == 'Polygon') {
      t.equal(gtype, 'Polygon', 'ok gtype');
    }
  }
  t.end();
});
