function ModuleInjectorCtrl($scope, ModuleService, $routeParams, $compile, $http, $timeout) {
  var moduleName = $routeParams.moduleName;

  // Load the current module
  var loadModule = function() {
    ModuleService.module(moduleName).then(function(module) {
      $scope.module = module;
    });
  };
  loadModule();

  var pollModule = function() {
    var update_rate = 1000;
    if($scope.module)
      update_rate = $scope.module.update_rate * 1000;

    $timeout(function() {
      loadModule();
      pollModule();
    }, update_rate);
  };
  pollModule();

  // Load the angular-like html to be injected
  $http.get('/api/modules/' + moduleName + '/public/partial.html').then(function(result) {
    $('#inject').html($compile(result.data)($scope));
  });
}

function ModuleFieldCtrl($scope, ModuleService, $timeout) {
  $scope.field.state = '';

  $scope.update = function() {
    var field = $scope.field;
    field.state = 'waiting';
    setTimeout(function() {
      var fade = function()  { console.log('fade'); $timeout(function() { field.state = ''; }, 2000); };
      ModuleService.updateField($scope.module, field, field.value).then(function(data) {
        console.log(data);
        if(data['success']) {
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
