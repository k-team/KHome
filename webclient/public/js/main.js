"use strict";

angular.module('GHome', ['ngRoute', 'ui.bootstrap', 'angularFileUpload', 'frapontillo.bootstrap-switch'])
  .config(function($routeProvider, $locationProvider, $httpProvider) {
    $routeProvider.when('/home', {
      templateUrl: '/partials/home.html'
    }).when('/store', {
      templateUrl: '/partials/store.html',
      controller: 'StoreCtrl'
    }).when('/settings', {
      templateUrl: '/partials/settings.html',
      controller: 'SettingsCtrl'
    }).when('/settings/:moduleName', {
      templateUrl: '/partials/module_settings.html'
    }).when('/modules', {
      templateUrl: '/partials/modules.html',
      controller: 'ModulesCtrl'
    }).when('/modules/:moduleName', {
      templateUrl: '/partials/module_inject.html',
      controller: 'ModuleInjectorCtrl'
    }).otherwise({
      redirectTo: '/home'
    });
  });
;function FieldCtrl($scope, $rootScope, ModuleService, $timeout) {
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
;function MainCtrl($scope, $location, ModuleService) {
  // All modules
  $scope.modules = [];

  // Explicitly reload modules
  $scope.reloadModules = function() {
    ModuleService.installed().then(function(modules) {
      $scope.modules = modules;
    });
  };

  $scope.$watch('query', function() {
    var path = $location.path();
    if ($scope.query && path != '/store' && path != '/modules') {
      $location.path('/modules');
    }
  });
}
;function ModuleInjectorCtrl($scope, ModuleService, $routeParams, $compile, $http, $timeout) {
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
  loadModule();//.then(pollFieldValue);

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
;function ModulesCtrl($scope, $location, ModuleService) {
  // Reload modules immediately
  $scope.reloadModules();

  // Uninstall a module
  $scope.uninstall = function(module) {
    //ModuleService.uninstall(module);
    console.log('uninstalling', module);
  };

  // Navigate to module view, either its specific view or configuration
  $scope.navigate = function(module) {
    $location.path('/modules/' + module.name);
  };
}
;function RatingCtrl($scope, ModuleService) {
  $scope.isRating = false;
  $scope.rate = function() {
    $scope.isRating = true;
    ModuleService.rate($scope.module, $scope.module.rating).then(function() {
      console.log('rating success');
    }, function() {
      console.log('rating error');
    }, function() {
      $scope.isRating = false;
    });
  };
}
;function SettingsCtrl($scope, $location) {
  $scope.reloadModules();

  $scope.navigate = function(module) {
    $location.path('/settings/' + module.id);
  };
}
;function StoreCtrl($scope, ModuleService, $modal, $timeout) {
  // All modules
  $scope.availableModules = [];

  // Explicitly reload modules
  $scope.reloadAvailableModules = function() {
    $scope.loading = true;
    ModuleService.available().then(function(modules) {
      $scope.availableModules = modules;
      $timeout(function() { $scope.loading = false; }, 1000);
      $scope.unreachable = false;
    }, function() {
      $timeout(function() { $scope.loading = false; }, 1000);
      $scope.unreachable = true;
    });
  };
  //...and call immediately
  $scope.reloadAvailableModules();

  // Install a module
  $scope.modulesInstalling = [];
  $scope.install = function(module) {
    for (var i = 0; i < $scope.modulesInstalling.length; i++) {
      if ($scope.modulesInstalling[i].id == module.id) {
        return;
      }
    }

    // Start installing
    $scope.modulesInstalling.push(module);
    ModuleService.installFromCatalog(module).then(function() {
    }, function() {
    }, function() {
      for (var i = 0; i < $scope.modulesInstalling.length; i++) {
        if ($scope.modulesInstalling[i].id == module.id) {
          $scope.modulesInstalling.splice(i, 1);
          break;
        }
      }
    });
  };

  // Uploading system
  $scope.uploading = false
  $scope.upload = function(file) {
    $scope.uploading = true;
    $scope.upload = ModuleService.installFromFile(file).progress(function(evt) {
      $scope.uploadProgress = parseInt(100.0 * evt.loaded / evt.total);
    }).success(function() {
      $scope.uploading = false;
      $scope.reloadAvailableModules();
    }).error(function() {
      $scope.uploading = false;
      // TODO handle errors better
    });
  };

  $scope.modalInstances = {};
  $scope.openModal = function(module) {
    var modalScope = $scope.$new(true);

    // Dismiss the modal
    modalScope.dismiss = function() {
      $scope.modalInstances[module.id].dismiss();
    };

    // Install the module
    modalScope.install = function() {
      $scope.install(module);
      modalScope.dismiss();
    };

    // Access the modal's module
    modalScope.module = module;

    // Open the modal
    $scope.modalInstances[module.id] = $modal.open({
      templateUrl: 'modal.html',
      scope: modalScope
    });
  };
}
;function SupervisionCtrl($scope, ModuleService, $timeout, $rootScope) {
  $scope.data = null;
  $scope.maxData = 100;
  var field = $scope.field;

  var addData = function(data) {
    // Empty data case
    if (!$scope.data) {
      $scope.data = {};
      $scope.data[field.name] = [];
    }

    // Verify if data should be added
    var fieldData = $scope.data[field.name];
    if (fieldData.length && fieldData[fieldData.length - 1][0] == data.time) { return; }

    // Push new data
    fieldData.push([data.time, data.value]);
    if ($scope.maxData < fieldData.length) {
      fieldData.splice(0, fieldData.length - $scope.maxData);
    }
  };

  ModuleService.fieldAllStatus($scope.moduleName, field.name).then(function(data) {
    data.forEach(addData);
  });

  // Poll the current supervised module for its status
  $scope.$on('fieldUpdate', function(_, fieldEmit, data) {
    if(field != fieldEmit) { return; }
    addData(data);
  });

  // Clear data when location is changed
  $rootScope.$on('$routeChangeSuccess', function () {
    $scope.data = null;
  });
}
;angular.module('GHome').directive('graph', function() {
  return {
    restrict: 'EA',
    link: function($scope, elem, attrs) {
      var color_r = (Math.random()*(200)|0).toString();
      var color_g = (Math.random()*(200)|0).toString();
      var color_b = (Math.random()*(200)|0).toString();

      var allData = [];
      var chart = null, opts = {
        xaxis: {
          tickSize: 1,
          tickFormatter: function(n) {
            function twoDigits(value) {
              if(value < 10) {
                return '0' + value;
              }
              return value;
            }
            var d = new Date(n * 1000);
            var h = twoDigits(d.getHours());
            var m = twoDigits(d.getMinutes());
            return h + ":" + m;
          },
        }, yaxis: {
          tickLength: 0
        }, grid: {
          borderWidth: 0,
          aboveData: true,
          markings: [ { yaxis: { from: 0, to: 0 }, color: '#888' },
                      { xaxis: { from: 0, to: 0 }, color: '#888' }]
        }, series: {
          color: "rgb(" + color_r + ", " + color_g + ", " + color_b + ")",
          shadowSize: 0,
          points: {
            show: true
          }, lines: {
            show: true,
            fill: 1.0,
            fillColor: "rgba(" + color_r + ", " + color_g + ", " + color_b + ", 0.25)"
          }
        }
      };

      // Actual plotting based on the graph data model
      $scope.$watch(attrs.graphModel, function(data) {
        var plottedData = []
        if (data instanceof Array) {
          plottedData = data;
        } else {
          angular.forEach(data, function(rawData, label) {
            plottedData.push({ label: label, data: rawData });
          });
        }

        if (!chart) {
          chart = $.plot(elem, plottedData, opts);
          elem.css('display', 'block');
        } else {
          chart.setData(plottedData);
          chart.setupGrid();
          chart.draw();
        }
        allData.concat(plottedData);
      }, true);

      // Set the tick size
      $scope.$watch(attrs.tickSize, function(tick) {
        opts.xaxis.tickSize = tick;
        chart = $.plot(elem, allData, opts);
      }, true);
    }
  };
});
;angular.module('GHome').directive('customInput', function() {
  return {
    restrict: 'EA',
    link: function($scope, elem, attrs) {
      $scope.$watch('field.state', function(state) {
        elem.children().fadeOut(500, function() {
          elem.children().find('.glyphicon-pencil').fadeIn(500);
          console.log(elem.children().find('.glyphicon-pencil'));
        });
      });
    }
  };
});
;angular.module('GHome').filter('graphable', function () {
  return function (fields){
    if (fields === undefined) {
      return;
    }

    var re = Array();
    for (var i = 0 ; i < fields.length ; i++) {
      var field = fields[i];
      if (field.readable && field.graphable) {
        re.push(field);
      }
    }
    return re;
  };
});

;angular.module('GHome').filter('truncate', function () {
  return function (text, length, end){
    if (text === undefined) {
      return;
    }

    // Default value for length
    if (isNaN(length)) { length = 10; }

    // Default value for end
    if (end === undefined) { end = '...'; }

    // Actual filter
    if (text.length <= length || text.length - end.length <= length) {
      return text;
    } else {
      return String(text).substring(0, length - end.length) + end;
    }
  };
});
;angular.module('GHome').factory('ModuleService', function($q, $http, $timeout, $upload) {
  var service = {},
    modulesUrl = '/api/modules',
    storeUrl = '/api/available_modules';

  var httpPostJSON = function(url, data) {
    var formattedData = '';
    for (var key in data) {
      formattedData += key + '=' + data[key] + '&';
    }
    formattedData = formattedData.substring(0, formattedData.length-1);
    return $http({
      url: url, method: 'POST', data: formattedData,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });
  };

  var httpGetJSON = function(url) {
    var deferred = $q.defer();
    $http.get(url)
      .success(function(data) { deferred.resolve(data); })
      .error(function() { deferred.reject(); });
    return deferred.promise;
  };

  service.module = function(name) {
    return httpGetJSON(modulesUrl + '/' + name);
  };

  service.moduleStatus = function(name) {
    return httpGetJSON(modulesUrl + '/' + name + '/instances/status');
  };

  service.fieldStatus = function(module_name, field_name) {
    return httpGetJSON(modulesUrl + '/' + module_name + '/fields/' + field_name + '/status');
  };

  service.fieldAllStatus = function(module_name, field_name) {
    return httpGetJSON(modulesUrl + '/' + module_name + '/fields/' + field_name + '/all-status');
  };

  service.updateField = function(module, field, value) {
    var deferred = $q.defer();
    httpPostJSON(modulesUrl + '/update_field',
        { name: module.name, field: field.name, value: value })
      .success(function(data) { deferred.resolve(data); })
      .error(function() { deferred.reject(); });
    return deferred.promise;
  };

  var getModules = function(url, cachedModules, forceReload) {
    var deferred = $q.defer();
    if (!forceReload) {
      $http.get(url).success(function(data) {
        cachedModules = data;
        deferred.resolve(data);
      }).error(function() { deferred.reject(); });
    } else {
      deferred.resolve(cachedModules);
    }
    return deferred.promise;
  };

  // Get the list of available modules, optionally passing if this should force
  // a reload of this list
  service.availableModules = [];
  service.available = function(forceReload) {
    return getModules(storeUrl, this.availableModules, forceReload);
  };

  service.rate = function(module, oldValue) {
    var value = parseInt(oldValue);
    if (!value || value < 1 || value > 5) {
      console.error('Invalid value', oldValue);
    }
    var deferred = $q.defer();
    httpPostJSON(storeUrl + '/rate', { name: module.name, value: value })
      .success(function() { deferred.resolve(); })
      .error(function() { deferred.reject(); });
    return deferred.promise;
  };

  // Get the list of installed modules, optionally passing if this should force
  // a reload of this list
  service.installedModules = [];
  service.installed = function(forceReload) {
    return getModules(modulesUrl, this.installedModules, forceReload);
  };

  // Install a module, passing in the uploaded file object (see $upload for
  // details). Return a promise object for the given upload http call.
  service.installFromFile = function(file) {
    return $upload.upload({
      url: modulesUrl + '/install',
      method: 'POST', file: file
    });
  }
  // ...from the catalog
  service.installFromCatalog = function(module) {
    var deferred = $q.defer();
    httpPostJSON(modulesUrl + '/install', { name: module.name })
      .success(function() { deferred.resolve(); })
      .error(function() { deferred.reject(); });
    return deferred.promise;
  }

  return service;
});
