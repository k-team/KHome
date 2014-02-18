function SupervisionCtrl($scope, ModuleService, $timeout, $rootScope) {
  $scope.data = null;
  $scope.maxData = 100;

  // Poll the current supervised module for its status
  $scope.$on('module.statusUpdate', function(_, data) {
    if (!data) { return; }
    data = [data]; // Hack !

    angular.forEach(data, function(instance) {
      for (var i = 0; i < instance.fields.length; i++) {
        var field = instance.fields[i];

        // Check if field is ok
        if (!field.readable || !field.graphable) { continue; }
        // if (!field.readable || field.type != 'numeric' || field.constant) { return; }

        var fieldFullName = instance.name + '.' + field.name;
        // Empty data case
        if (!$scope.data) {
          $scope.data = {};
        }
        if (!$scope.data[fieldFullName]) {
          $scope.data[fieldFullName] = [];
        }

        // Verify if data should be added
        var fieldData = $scope.data[fieldFullName];
        if (fieldData.length && fieldData[fieldData.length - 1][0] == field.time) { continue; }

        // Push new data
        fieldData.push([field.time, field.value]);
        if ($scope.maxData < fieldData.length) {
          fieldData.splice(0, fieldData.length - $scope.maxData);
        }
      }
    });
  });

  // Clear data when location is changed
  $rootScope.$on('$routeChangeSuccess', function () {
    $scope.data = null;
  });
}
