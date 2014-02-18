function SupervisionCtrl($scope, ModuleService, $timeout, $rootScope) {
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

    // Poll the current supervised module for its status
    poll = pollModule($scope.moduleName, function(promise) {
      promise.then(function(data) {
        data = [data];
        angular.forEach(data, function(instance) {
          angular.forEach(instance.fields, function(data, field) {
            var attrName = instance.name + '.' + field;
            // Empty data case
            if (!$scope.data[attrName]) {
              $scope.data[attrName] = [];
            }

            // Push new data
            var attrData = $scope.data[attrName];
            attrData.push([data.time, data.value]);
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
    $rootScope.$on('$routeChangeSuccess', function () {
      poll.cancel();
      $scope.data = {};
      $scope.graphData = [];
    });
  });
}
