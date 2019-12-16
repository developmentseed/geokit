var fs = require('fs');
var turf = require('@turf/turf');
var _ = require('underscore');
var cover = require('@mapbox/tile-cover');
var rbush = require('rbush');
var mkdirp = require('mkdirp');
var path = require('path');
module.exports = function (file, folder, zoom) {
  var points = JSON.parse(fs.readFileSync(file, 'utf8'));
  var result = pro(points, zoom);
  var objGrid = {};
  var outputPoints = {};
  _.each(result, function (v, k) {
    if (v && v.grid && v.features) {
      objGrid[k] = v.grid;
      outputPoints[k] = v.features;
    }
  });
  mkdirp(path.join(process.cwd(), folder), function (err) {
    if (err) {
      return console.error(err);
    }
    
  });
  fs.writeFileSync(
    file.split('.')[0] + '-' + zoom + '-grid.geojson',
    JSON.stringify(turf.featureCollection(_.values(objGrid)))
  );
  for (var grid in outputPoints) {
    var objs = {
      type: 'FeatureCollection',
      features: outputPoints[grid]
    };
    fs.writeFileSync(folder + '/' + grid + '.geojson', JSON.stringify(objs));
  }
};

function pro(points, zoom) {
  var totalOutput = {};
  pre(points, zoom);

  function pre(Pointsfeatures, z) {
    console.log('Processing zoom: ' + z);
    var bboxPolygon = turf.bboxPolygon(turf.bbox(Pointsfeatures));
    var output = {};
    var limits = {
      min_zoom: z,
      max_zoom: z
    };
    var polys = cover.geojson(bboxPolygon.geometry, limits);
    var tiles = cover.tiles(bboxPolygon.geometry, limits);
    var bboxesPolys = [];
    var bboxesPoints = [];

    var objects = {};
    for (var k = 0; k < polys.features.length; k++) {
      var poly = polys.features[k];
      poly.properties.id = tiles[k].join('');
      bboxesPolys.push(objBbox(poly));
      objects[poly.properties.id] = poly;
    }
    for (var p = 0; p < Pointsfeatures.features.length; p++) {
      var pt = Pointsfeatures.features[p];
      var id = p + 'p';
      bboxesPoints.push(objBbox(pt, p + 'p'));
      objects[id] = pt;
    }
    var bboxes = bboxesPoints.concat(bboxesPolys);
    var tree = rbush(bboxes.length);
    tree.load(bboxes);
    for (var j = 0; j < bboxesPolys.length; j++) {
      var bbox = bboxesPolys[j];
      var feature = objects[bbox.id];
      if (feature.geometry.type === 'Polygon') {
        var overlaps = tree.search(bbox);
        for (var i = 0; i < overlaps.length; i++) {
          overlap = overlaps[i];
          if (overlap.id !== bbox.id) {
            var point = objects[overlap.id];
            if (point.geometry.type === 'Point') {
              if (turf.inside(point, feature)) {
                if (output[feature.properties.id]) {
                  output[feature.properties.id].features.push(point);
                } else {
                  output.features = {};
                  output[feature.properties.id] = {};
                  output[feature.properties.id].features = [point];
                  output[feature.properties.id].grid = feature;
                }
              }
            }
          }
        }
      }
    }
    _.each(output, function (v, k) {
      if (v.features && v.features.length > 40 && z <= 15) {
        pre(turf.featureCollection(v.features), z + 1);
      } else {
        totalOutput[k] = v;
      }
    });
  }
  return totalOutput;
}

function objBbox(feature, id) {
  var bboxExtent = ['minX', 'minY', 'maxX', 'maxY'];
  var bbox = {};
  var valBbox = turf.bbox(feature);
  for (var d = 0; d < valBbox.length; d++) {
    bbox[bboxExtent[d]] = valBbox[d];
  }
  bbox.id = id || feature.properties.id;
  return bbox;
}
