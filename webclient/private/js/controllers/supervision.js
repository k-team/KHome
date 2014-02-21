function SupervisionCtrl($scope, ModuleService, $timeout, $rootScope) {
  $scope.data = null;
  $scope.maxData = 100;
  var field = $scope.field;

  var addData = function(data) {
    // Empty data case
    if (!$scope.data) {
      $scope.data = {};
      $scope.data[field.public_name] = [];
    }

    // Verify if data should be added
    var fieldData = $scope.data[field.public_name];
    if (fieldData.length && fieldData[fieldData.length - 1][0] == data.time) { return; }

    // Push new data
    fieldData.push([data.time, data.value]);
    if ($scope.maxData < fieldData.length) {
      fieldData.splice(0, fieldData.length - $scope.maxData);
    }
  };

  ModuleService.fieldAllStatus($scope.moduleName, field.name).then(function(data) {
    data.forEach(addData);
  });

  // Poll the current supervised module for its status
  $scope.$on('fieldUpdate', function(_, fieldEmit, data) {
    if(field != fieldEmit) { return; }
    addData(data);
  });

  // Clear data when location is changed
  $rootScope.$on('$routeChangeSuccess', function () {
    $scope.data = null;
  });
}
