function ModuleInjectorCtrl($scope, ModuleService, $routeParams, $compile, $http) {
  $scope.moduleName = $routeParams.moduleName;
  $scope.module = null;

  // Load the current module
  var loadModule = function() {
    return ModuleService.moduleStatus($scope.moduleName).then(function(module) {
      $scope.module = module;
      $scope.$broadcast('module.statusUpdate', module);
      return module;
    });
  };

  var loadFieldValue = function() {
    return ModuleService.moduleStatus($scope.moduleName).then(function(module) {
      for (var i = 0; i < module.fields.length; i++) {
        $scope.module.fields[i].time = module.fields[i].time;
        $scope.module.fields[i].value = module.fields[i].value;
      }
      $scope.$broadcast('module.statusUpdate', module);
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
