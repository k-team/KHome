function ModuleInjectorCtrl($scope, ModuleService, $routeParams, $compile, $http) {
  $scope.moduleName = $routeParams.moduleName;
  $scope.module = null;

  // Load the current module
  var loadModule = function() {
    $scope.loading = true;
    return ModuleService.moduleStatus($scope.moduleName).then(function(module) {
      $scope.loading = false;
      $scope.unreachable = false;
      $scope.module = module;
      $scope.$broadcast('module.statusUpdate', module);
      return module;
    }, function() {
      $scope.loading = false;
      $scope.unreachable = true;
    });
  };
  // Start polling
  loadModule();

  // Load the angular-like html to be injected
  $http.get('/api/modules/' + $scope.moduleName + '/public/partial.html')
    .then(function(result) { $('#inject').html($compile(result.data)($scope)); });
  $http.get('/api/modules/' + $scope.moduleName + '/public/independant.html')
    .then(function(result) { $('#inject-independant').html($compile(result.data)($scope)); });
}
