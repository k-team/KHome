function ModuleInjectorCtrl($scope, $route, $routeParams, $http, $compile) {
  $route.current.templateUrl = '/api/modules/'
    + $routeParams.moduleName
    + '/public/partial.html';

  // Note: this is a hack, but it works
  $.get($route.current.templateUrl, function(data) {
    $('#inject').html($compile(data)($scope));
  });
}
