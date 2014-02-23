angular.module('GHome').filter('visible', function () {
  return function (modules) {
    if (modules === undefined) {
      return;
    }

    var re = Array();
    for (var i = 0 ; i < modules.length ; i++) {
      var module = modules[i];
      if (module.has_view === true || module.has_view === undefined) {
        re.push(module);
      }
    }
    return re;
  };
});

angular.module('GHome').filter('fieldVisible', function () {
  return function (fields) {
    if (fields === undefined) {
      return;
    }

    var re = Array();
    for (var i = 0 ; i < fields.length ; i++) {
      var field = fields[i];
      if ((field.writable || field.readable)
        && field.type !== undefined
        && (field.type == 'string' ||
            field.type == 'numeric' ||
            field.type == 'boolean')) {
        re.push(field);
      }
    }
    return re;
  };
});
