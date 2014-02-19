angular.module('GHome').filter('graphable', function () {
  return function (fields){
    if (fields === undefined) {
      return;
    }

    var re = Array();
    for (var i = 0 ; i < fields.length ; i++) {
      var field = fields[i];
      if (field.readable && field.graphable) {
        re.push(field);
      }
    }
    return re;
  };
});

