const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const bbox2fc = require('../src/bbox2fc.js');
const FeatureCollection = { "type": "FeatureCollection", "features": [{ "type": "Feature", "properties": {}, "geometry": { "type": "Polygon", "coordinates": [[[7.409527301788444, 43.72263717651373], [7.440137863159237, 43.72263717651373], [7.440137863159237, 43.750888824463004], [7.409527301788444, 43.750888824463004], [7.409527301788444, 43.72263717651373]]] } }] };
test('Bbox2fc', function (t) {
    t.plan(1);
    logInterceptor();
    bbox2fc(`7.409527301788444, 43.72263717651373, 7.440137863159237, 43.750888824463004`);
    let logs = logInterceptor.end();
    const fc = JSON.parse(logs[0]);
    t.deepEqual(fc, FeatureCollection, 'ok FeatureCollection');
    t.end();
});