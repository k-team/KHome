function ModuleInjectorCtrl($scope, ModuleService, $routeParams, $compile, $http, $timeout) {
  $scope.moduleName = $routeParams.moduleName;
  $scope.module = null;

  // Load the current module
  var loadModule = function() {
    return ModuleService.moduleStatus($scope.moduleName).then(function(module) {
      $scope.module = module;
      $scope.$broadcast('module.statusUpdate', module);
      return module;
    });
  };

  var loadFieldValue = function() {
    return ModuleService.moduleStatus($scope.moduleName).then(function(module) {
      for (var i = 0; i < module.fields.length; i++) {
        $scope.module.fields[i].time = module.fields[i].time;
        $scope.module.fields[i].value = module.fields[i].value;
      }
      $scope.$broadcast('module.statusUpdate', module);
    });
  };

  // Poll the current module for its status
  var pollFieldValue = function() {
    var updateRate = 1, poll = $timeout(function doPoll() {
      loadFieldValue().then(function(module) {
        if (module) { updateRate = module['update_rate']; }
        poll = $timeout(doPoll, 1000*updateRate);
      });
    }, 1000*updateRate);

    $scope.$on('$routeChangeSuccess', function () {
      $timeout.cancel(poll);
    });
  };

  // Start polling
  loadModule().then(pollFieldValue);

  // Load the angular-like html to be injected
  $http.get('/api/modules/' + $scope.moduleName + '/public/partial.html')
    .then(function(result) { $('#inject').html($compile(result.data)($scope)); });
  $http.get('/api/modules/' + $scope.moduleName + '/public/independant.html')
    .then(function(result) { $('#inject-independant').html($compile(result.data)($scope)); });
}

function ModuleFieldCtrl($scope, ModuleService, $timeout) {
  $scope.field.state = '';
  $scope.update = function() {
    $scope.field.state = 'waiting';

    // Fade out field state
    var fade = function()  { $timeout(function() { $scope.field.state = ''; }, 2000); };

    // Call update
    ModuleService.updateField($scope.module, $scope.field, $scope.field.value).then(function(data) {
      $scope.field.state = (data.success) ? 'success' : 'error';
      fade();
    }, function() {
      $scope.field.state = 'error';
      fade();
    });
  };
}
