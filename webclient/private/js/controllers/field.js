function FieldCtrl($scope, $rootScope, ModuleService, $timeout) {
  $scope.state = '';

  $scope.update = function() {
    $scope.state = 'waiting';

    // Fade out field state
    var fade = function()  { $timeout(function() {
      $scope.state = '';
    }, 2000); };

    // Call update
    ModuleService.updateField($scope.module, $scope.field, $scope.field.value).then(function(data) {
      $scope.state = (data.success) ? 'success' : 'error';
      fade();
    }, function() {
      $scope.state = 'error';
      fade();
    });
  };

  var loadValue = function() {
    return ModuleService.fieldStatus($scope.moduleName, $scope.field.name).then(function(data) {
      $scope.field.value = data.value;

      // Super hack
      $rootScope.$broadcast('fieldUpdate', $scope.field, data);
    });
  };

  // Poll the current module for its status
  var pollValue = function() {
    // var updateRate = $scope.module['update_rate'];
    var updateRate = $scope.field['update_rate'];
    var poll = $timeout(function doPoll() {
      loadValue().then(function() {
        poll = $timeout(doPoll, 1000*updateRate);
      });
    }, 1000*updateRate);

    $scope.$on('$destroy', function () {
      $timeout.cancel(poll);
    });
  };

  pollValue();
}
