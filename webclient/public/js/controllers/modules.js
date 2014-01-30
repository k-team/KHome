function ModulesCtrl($scope, ModuleService) {
  // All modules
  $scope.modules = [];

  // Explicitly reload modules
  $scope.reloadModules = function() {
    ModuleService.installed().then(function(modules) {
      $scope.modules = modules;
    });
  };
  //...and call immediately
  $scope.reloadModules();
}
