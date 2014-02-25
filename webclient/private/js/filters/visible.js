angular.module('GHome').filter('moduleVisible', function () {
  return function (modules) {
    if (modules === undefined) {
      return;
    }

    var re = Array();
    for (var i = 0 ; i < modules.length ; i++) {
      var module = modules[i];
      // if ((module.has_view === true || module.has_view === undefined)
      //   && module.public_name != '' && module.public_name !== undefined) {
        re.push(module);
      // }
      // else {
      //   re.push(module);
      // }
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

angular.module('GHome').filter('fieldSorted', function () {
  return function (fields) {
    if (fields === undefined) {
      return;
    }

    return fields.sort(function(a, b) {
      if (a.writable && !b.writable) {
        return 1;
      }
      if (!a.writable && b.writable) {
        return -1;
      }
      if (a.type == 'boolean' && b.type != 'boolean') {
        return 1;
      }
      if (a.type != 'boolean' && b.type == 'boolean') {
        return -1;
      }
      if (a.type == 'numeric' && b.type != 'numeric') {
        return 1;
      }
      if (a.type != 'numeric' && b.type == 'numeric') {
        return -1;
      }
      return a.public_name > b.public_name ? 1 : -1;
    })
  };
});
