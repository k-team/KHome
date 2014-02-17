function SupervisionCtrl($scope, ModuleService, $timeout) {
  $scope.data = {};
  $scope.maxData = 10;

  // Poll all module instances for their statuses, passing in the module's name
  // and a callback which should be applied on a $http promise object.
  // Optionally, pass in the delay to override the service's default polling
  // delay.
  var pollInstances = function(name, callback, delay) {
    if (delay === undefined) { delay = 1000; }

    var timeout = $timeout(function pollFn() {
      callback(ModuleService.module(name));
      timeout = $timeout(pollFn, delay);
    }, delay);

    return {
      cancel: function() {
        $timeout.cancel(timeout);
      }
    };
  };

  $scope.$watch('module', function() {
    // Cancel the previous poll
    if ($scope.poll) {
      $scope.poll.cancel();
      $scope.data = {};
    }

    // Do nothing if the module isn't set
    if (!$scope.module) { return; }

    // Poll the current supervised module for its status
    $scope.poll = pollInstances($scope.module, function(promise) {
      promise.then(function(data) {
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
      }, function() {
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
