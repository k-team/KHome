function SettingsCtrl($scope, $location) {
  $scope.reloadModules();

  $scope.navigate = function(module) {
    $location.path('/settings/' + module.id);
  };
}
