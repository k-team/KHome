function SupervisionCtrl($scope, ModuleService) {
  $scope.module = '';
  $scope.data = {};
  $scope.maxData = 10;
  $scope.poll = null;

  $scope.$watch('module', function() {
    // Cancel the previous poll
    if ($scope.poll) {
      $scope.poll.cancel();
      $scope.data = {};
    }

    // Do nothing if the module isn't set
    if (!$scope.module) { return; }

    // Poll the current supervised module for its status
    $scope.poll = ModuleService.pollInstances($scope.module, function(promise) {
      promise.success(function(data) {
        angular.forEach(data, function(instance) {
          var instanceName = instance.name;
          angular.forEach(instance.attrs, function(data, attr) {
            var attrName = instanceName + '.' + attr
            // Empty data case
            if (!$scope.data[attrName]) {
              $scope.data[attrName] = [];
            }

            // Push new data
            var attrData = $scope.data[attrName];
            attrData.push([instance.time, data]);
            if ($scope.maxData < attrData.length) {
              attrData.splice(0, attrData.length - $scope.maxData);
            }
          });
        });
      }).error(function() {
        // TODO
      });
    });

    // Stop polling when location is changed
    $scope.$on('$routeChangeSuccess', function () {
      $scope.poll.cancel();
      $scope.module = '';
      $scope.data = {};
      $scope.graphData = [];
    });
  });
}
