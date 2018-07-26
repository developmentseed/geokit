var fs = require('fs');
var turf = require('@turf/turf');
module.exports = function(file) {

  var obj = JSON.parse(fs.readFileSync(file).toString());

  for (var i = 0; i < obj.features.length; i++) {

    var areafeature = turf.area(obj.features[i]);
    areafeatureha = ((areafeature / 1000000) * 100).toFixed(0);
    obj.features[i].properties.area = areafeatureha + "ha";

  }
  console.log(JSON.stringify(obj));
};
