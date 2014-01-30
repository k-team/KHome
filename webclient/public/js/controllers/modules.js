function ModulesCtrl($scope, ModuleService) {
  // All modules
  $scope.modules = [];

  // Explicitly reload modules
  $scope.reloadModules = function() {
    ModuleService.all().then(function(modules) {
      $scope.modules = modules;
    });
  };
  //...and call immediately
  $scope.reloadModules();

  // Uploading system
  $scope.uploading = false
  $scope.upload = function(file) {
    $scope.uploading = true;
    $scope.upload = ModuleService.install(file).progress(function(evt) {
      $scope.uploadProgress = parseInt(100.0 * evt.loaded / evt.total);
    }).success(function() {
      $scope.uploading = false;
      $scope.reloadModules();
    }).error(function() {
      $scope.uploading = false;
      // TODO handle errors better
    });
  };

  // Toggle module visibilité/activity
  $scope.expandedModule = null;
  $scope.toggleActiveModule = function(module) {
    if ($scope.expandedModule == module) {
      $scope.expandedModule = null;
    } else {
      $scope.expandedModule = module;
    }
  };
}
