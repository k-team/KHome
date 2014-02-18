function MainCtrl($scope, $location, ModuleService) {
  // All modules
  $scope.modules = [];

  // Explicitly reload modules
  $scope.reloadModules = function() {
    ModuleService.installed().then(function(modules) {
      $scope.modules = modules;
    });
  };

  $scope.$watch('query', function() {
    var path = $location.path();
    if ($scope.query && path != '/store' && path != '/modules') {
      $location.path('/modules');
    }
  });
}
