function GraphCtrl($scope, ModulePolling) {
  $scope.data = [];

  var poll = ModulePolling.poll('t_module_1', function(promise) {
    promise.success(function(data) {
      $scope.data.push([data.time, data.temperature]);
    });
  });

  $scope.$on('$destroy', function() {
    poll.cancel();
  });
}
