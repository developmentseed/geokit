const test = require('tape');
const logInterceptor = require('log-interceptor');
const path = require('path');
const cmd = require('../index.js');
const file = path.join(__dirname, '/fixtures/monaco.geojson');
test('Bbox', function (t) {
    t.plan(2);
    logInterceptor();
    cmd.bbox(file);
    let logs = logInterceptor.end();
    const bbox = JSON.parse(logs[0]);
    t.equal(bbox.length, 4, 'Array size 4');
    t.deepEqual(bbox, [7.409527301788444, 43.72263717651373, 7.440137863159237, 43.750888824463004], 'Ok array');
    t.end();
});