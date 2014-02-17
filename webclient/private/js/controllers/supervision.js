function SupervisionCtrl($scope, ModuleService, $timeout) {
  $scope.data = {};
  $scope.maxData = 10;

  var pollModule = function(name, callback, delay) {
    if (delay === undefined) { delay = 1000; }

    var timeout = $timeout(function pollFn() {
      callback(ModuleService.moduleStatus(name));
      timeout = $timeout(pollFn, delay);
    }, delay);

    return {
      cancel: function() {
        $timeout.cancel(timeout);
      }
    };
  };

  var poll = null;
  $scope.$watch('moduleName', function() {
    // Cancel the previous poll
    if (poll) {
      poll.cancel();
      $scope.data = {};
    }

    // Do nothing if the module isn't set
    if (!$scope.moduleName) { return; }
    console.log('moduleName', $scope.moduleName);

    // Poll the current supervised module for its status
    poll = pollModule($scope.moduleName, function(promise) {
      promise.then(function(data) {
        console.log('poll got', data);
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
        console.log('poll failed');
      });
    });

    // Stop polling when location is changed
    $scope.$on('$routeChangeSuccess', function () {
      poll.cancel();
      $scope.data = {};
      $scope.graphData = [];
    });
  });
}
