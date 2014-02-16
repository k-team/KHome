function ModuleInjectorCtrl($scope, ModuleService, $routeParams, $compile, $http) {
  var moduleName = $routeParams.moduleName;

  // Load the current module
  ModuleService.module(moduleName).then(function(module) {
    $scope.module = module;
  });

  // Load the angular-like html to be injected
  $http.get('/api/modules/' + moduleName + '/public/partial.html').then(function(result) {
    $('#inject').html($compile(result.data)($scope));
  });
}

function ModuleFieldCtrl($scope, ModuleService, $timeout) {
  $scope.field.state = '';
  $scope.update = function(value) {
    var field = $scope.field;
    field.state = 'waiting';
    setTimeout(function() {
      var fade = function()  { console.log('fade'); $timeout(function() { field.state = ''; }, 2000); };
      ModuleService.updateField($scope.module, field, value).then(function() {
        field.state = 'success';
        fade();
      }, function() {
        field.state = 'error';
        fade();
      });
    }, 500);
  };
}
