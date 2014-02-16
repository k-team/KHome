function ModuleInjectorCtrl($scope, ModuleService, $routeParams, $compile, $http) {
  var moduleName = $routeParams.moduleName;

  // Load the current module
  ModuleService.module(moduleName).then(function(module) {
    // module.fields[0].state = 'success';
    $scope.module = module;
  });

  // Load the angular-like html to be injected
  $http.get('/api/modules/' + moduleName + '/public/partial.html').then(function(result) {
    $('#inject').html($compile(result.data)($scope));
  });
}
