function StoreCtrl($scope, ModuleService) {
  // All modules
  $scope.modules = [];

  // Explicitly reload modules
  $scope.reloadModules = function() {
    ModuleService.available().then(function(modules) {
      $scope.modules = modules;
    });
  };
  //...and call immediately
  $scope.reloadModules();

  // Install a module
  $scope.install = function(module) {
    console.log('installing module', module);
  };

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
}
