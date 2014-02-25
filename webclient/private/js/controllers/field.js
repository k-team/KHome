function FieldCtrl($scope, ModuleService, $rootScope, $timeout) {
  $scope.state = '';

  $scope.startEditing = function() {
    if ($scope.field && $scope.field.writable) {
      $scope.state = 'editing';
    }
  };

  $scope.undoEditing = function() {
    $scope.state = '';
  };

  $scope.update = function() {
    $scope.state = 'waiting';

    // Fade out field state
    var fade = function()  { $timeout(function() {
      $scope.state = '';
    }, 2000); };

    var value = $scope.field.value;
    if ($scope.field.type == 'boolean') {
      if (value == 'true')
        value = true;
      else if (value == 'false')
        value = false;
    }
    console.log(value);

    // Call update
    ModuleService.updateField($scope.module, $scope.field, value).then(function(data) {
      $scope.state = (data.success) ? 'success' : 'error';
      fade();
    }, function() {
      $scope.state = 'error';
      fade();
    });
  };

  var loadValue = function() {
    return ModuleService.fieldStatus($scope.moduleName, $scope.field.name).then(function(data) {
      if ($scope.state != 'editing') {
        if ($scope.field.type == 'boolean') {
          if (data.value) {
            $scope.field.value = true;
          }
          else
            $scope.field.value = false;
        }
        else {
          $scope.field.value = data.value;
        }
      }
      $rootScope.$broadcast('fieldUpdate', $scope.field, data);
    });
  };

  // Poll the current module for its status
  var pollValue = function() {
    // Update rate for poll
    var updateRate = $scope.field['update_rate'] || 1;

    var poll = $timeout(function doPoll() {
      loadValue().then(function() {
        poll = $timeout(doPoll, 1000*updateRate);
      });
    }, 1000*updateRate);

    $scope.$on('$destroy', function () {
      $timeout.cancel(poll);
    });
  };

  loadValue().then(function() { pollValue(); });
}
