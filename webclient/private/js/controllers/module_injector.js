function ModuleInjectorCtrl($scope, ModuleService, $routeParams, $compile, $http, $timeout) {
  var moduleName = $routeParams.moduleName;
  $scope.module = undefined;

  // Load the current module
  var loadModule = function() {
    ModuleService.module(moduleName).then(function(module) {
      $scope.module = module;
      $scope.module.show = true;
    });
  };
  loadModule();

  // Poll the current module for its status
  var pollModule = function() {
    var update_rate = 1, poll = $timeout(function() {
      loadModule();
      if ($scope.module) {
        update_rate = $scope.module.update_rate;
      }
      poll = $timeout(poll, 1000*update_rate);
    }, 1000*update_rate);

    $scope.$on('$routeChangeSuccess', function () {
      $timeout.cancel(poll);
    });
  };
  pollModule();

  // Load the angular-like html to be injected
  $http.get('/api/modules/' + moduleName + '/public/partial.html').then(function(result) {
    $('#inject').html($compile(result.data)($scope));
  });

  // Load the angular-like html to be injected
  $http.get('/api/modules/' + moduleName + '/public/independant.html').then(function(result) {
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
