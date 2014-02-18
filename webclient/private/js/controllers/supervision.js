function SupervisionCtrl($scope, ModuleService, $timeout, $rootScope) {
  $scope.data = null;
  $scope.maxData = 100;

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
          for (var i = 0; i < instance.fields.length; i++) {
            var field = instance.fields[i];

            // Check if field is ok
            if (!field.readable || field.type != 'numeric' || field.constant) { return; }

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
            if (fieldData.length && fieldData[fieldData.length - 1][0] == field.time) { return; }

            // Push new data
            fieldData.push([field.time, field.value]);
            if ($scope.maxData < fieldData.length) {
              fieldData.splice(0, fieldData.length - $scope.maxData);
            }
          }
        });
      }, function() {
        // TODO
      });
    });

    // Stop polling when location is changed
    $rootScope.$on('$routeChangeSuccess', function () {
      poll.cancel();
      $scope.data = null;
    });
  });
}
