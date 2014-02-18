function ModuleInjectorCtrl($scope, ModuleService, $routeParams, $compile, $http, $timeout) {
  $scope.module = undefined;
  $scope.moduleName = $routeParams.moduleName;

  // Load the current module
  var loadModule = function() {
    ModuleService.module($scope.moduleName).then(function(module) {
      $scope.module = module;
      $scope.module.show = true;
      console.log(module);
    });
  };
  loadModule();

  // Poll the current module for its status
  var pollModule = function() {
    var updateRate = 1, poll = $timeout(function() {
      loadModule();
      if ($scope.module) {
        updateRate = $scope.module.updateRate;
      }
      poll = $timeout(poll, 1000*updateRate);
    }, 1000*updateRate);

    $scope.$on('$routeChangeSuccess', function () {
      $timeout.cancel(poll);
    });
  };
  pollModule();

  // Load the angular-like html to be injected
  $http.get('/api/modules/' + $scope.moduleName + '/public/partial.html').then(function(result) {
    $('#inject').html($compile(result.data)($scope));
  });

  // Load the angular-like html to be injected
  $http.get('/api/modules/' + $scope.moduleName + '/public/independant.html').then(function(result) {
    $('#inject-independant').html($compile(result.data)($scope));
  });
}

function ModuleFieldCtrl($scope, ModuleService, $timeout) {
  $scope.field.state = '';

  $scope.update = function() {
    var field = $scope.field;
    field.state = 'waiting';
    setTimeout(function() {
      // Fade out field state
      var fade = function()  {
        $timeout(function() { field.state = ''; }, 2000);
      };

      ModuleService.updateField($scope.module, field, field.value).then(function(data) {
        if (data.success) {
          field.state = 'success';
        } else {
          field.state = 'error';
        }
        fade();
      }, function() {
        field.state = 'error';
        fade();
      });
    }, 500);
  };
}
