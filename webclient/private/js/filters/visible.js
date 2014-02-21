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


