function ModulesCtrl($scope, $location, ModuleService) {
  // Reload modules immediately
  $scope.reloadModules();

  // Uninstall a module
  $scope.uninstall = function(module) {
    //ModuleService.uninstall(module);
    console.log('uninstalling', module);
  };

  // Navigate to module view, either its specific view or configuration
  $scope.navigate = function(module) {
    console.log(module);
    $location.path('/modules/' + module.name);
  };
}
