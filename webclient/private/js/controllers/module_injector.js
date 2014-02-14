function ModuleInjectorCtrl($scope, $routeParams, $compile, $http) {
  $scope.moduleName = $routeParams.moduleName;
  $scope.templateUrl = '/api/modules/' + $scope.moduleName
    + '/public/partial.html';

  $http.get($scope.templateUrl).then(function(result){
    $scope.moduleContent = result.data;

    // Note: this is a hack, but it works
    $('#inject').html($compile(result.data)($scope));
  });
}
