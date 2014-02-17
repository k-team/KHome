"use strict";

angular.module('GHome', ['ngRoute', 'ngAnimate', 'ui.bootstrap', 'angularFileUpload', 'frapontillo.bootstrap-switch'])
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
;function MainCtrl($scope, ModuleService, HouseMapService) {
  // All modules
  $scope.modules = [];

  // Explicitly reload modules
  $scope.reloadModules = function() {
    ModuleService.installed().then(function(modules) {
      $scope.modules = modules;
    });
  };

  // Get the rooms (asynchronous)
  HouseMapService.getRooms().then(function(rooms) {
    $scope.rooms = rooms;
  });
}
;function ModuleInjectorCtrl($scope, ModuleService, $routeParams, $compile, $http, $timeout) {
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
;function ModulesCtrl($scope, $location, ModuleService) {
  // Reload modules immediately
  $scope.reloadModules();

  // Uninstall a module
  $scope.uninstall = function(module) {
    console.log('uninstalling', module);
  };

  // Navigate to module view, either its specific view or configuration
  $scope.navigate = function(module) {
    $location.path('/modules/' + module.id);
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
;function RoomsCtrl($scope) {
  // Minimal bbox af all rooms
  $scope.box = {};

  // Comma-separated representation for points (x1,y1 x2,y2 x3,y3 etc...), used
  // for svg rendering.
  $scope.points = function(room) {
    var pointsRepr = '';
    angular.forEach(room.polygon, function(point, i) {
      // Update the points representation
      pointsRepr += point.x + ',' + point.y;
      if (i < room.polygon.length - 1) {
        pointsRepr += ' ';
      }
    });
    return pointsRepr;
  };

  // Watch expression on rooms in order to update the bbox accordingly
  $scope.$watch('rooms', function() {
    angular.forEach($scope.rooms, function(room) {
      angular.forEach(room.polygon, function(point) {
        if      ($scope.box.minX === undefined || point.x < $scope.box.minX) { $scope.box.minX = point.x; }
        else if ($scope.box.maxX === undefined || point.x > $scope.box.maxX) { $scope.box.maxX = point.x; }
        if      ($scope.box.minY === undefined || point.y < $scope.box.minY) { $scope.box.minY = point.y; }
        else if ($scope.box.maxY === undefined || point.y > $scope.box.maxY) { $scope.box.maxY = point.y; }
      });
    });
  });
}
;function SettingsCtrl($scope, $location) {
  $scope.reloadModules();

  $scope.navigate = function(module) {
    $location.path('/settings/' + module.id);
  };
}
;function StoreCtrl($scope, $modal, ModuleService) {
  // All modules
  $scope.availableModules = [];

  // Explicitly reload modules
  $scope.reloadAvailableModules = function() {
    ModuleService.available().then(function(modules) {
      $scope.availableModules = modules;
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
;function SupervisionCtrl($scope, ModuleService) {
  $scope.module = '';
  $scope.data = {};
  $scope.maxData = 10;
  $scope.poll = null;

  $scope.$watch('module', function() {
    // Cancel the previous poll
    if ($scope.poll) {
      $scope.poll.cancel();
      $scope.data = {};
    }

    // Do nothing if the module isn't set
    if (!$scope.module) { return; }

    // Poll the current supervised module for its status
    $scope.poll = ModuleService.pollInstances($scope.module, function(promise) {
      promise.success(function(data) {
        angular.forEach(data, function(instance) {
          var instanceName = instance.name;
          angular.forEach(instance.attrs, function(data, attr) {
            var attrName = instanceName + '.' + attr
            // Empty data case
            if (!$scope.data[attrName]) {
              $scope.data[attrName] = [];
            }

            // Push new data
            var attrData = $scope.data[attrName];
            attrData.push([instance.time, data]);
            if ($scope.maxData < attrData.length) {
              attrData.splice(0, attrData.length - $scope.maxData);
            }
          });
        });
      }).error(function() {
        // TODO
      });
    });

    // Stop polling when location is changed
    $scope.$on('$routeChangeSuccess', function () {
      $scope.poll.cancel();
      $scope.module = '';
      $scope.data = {};
      $scope.graphData = [];
    });
  });
}
;angular.module('GHome').directive('graph', function() {
  return {
    restrict: 'EA',
    link: function($scope, elem, attrs) {
      var chart = null, opts = {
        xaxis: {
          tickLength: 0
        }, yaxis: {
          tickLength: 0
        }, grid: {
          borderWidth: 0,
          aboveData: true,
          markings: [ { yaxis: { from: 0, to: 0 }, color: '#888' },
                      { xaxis: { from: 0, to: 0 }, color: '#888' }]
        }, series: {
          shadowSize: 0,
          points: {
            show: true
          }, lines: {
            show: true
          }
        }
      };

      // Actual plotting based on the graph data model
      $scope.$watch(attrs.graphModel, function(data) {
        var plottedData = [];
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
;angular.module('GHome').directive('svgVbox', function() {
  return {
    link: function($scope, elem, attrs) {
      // Configurable viewBox padding
      var paddingRatio = 0.05;
      attrs.$observe('svgVboxPadding', function(value) {
        if (value === undefined) { return; }
        paddingRatio = parseFloat($scope.$eval(value));
      });

      $scope.$watch(attrs.svgVbox, function(vbox) {
        // Default values for viewBox
        if (vbox.minX === undefined) { vbox.minX = 0; }
        if (vbox.maxX === undefined) { vbox.maxX = 0; }
        if (vbox.minY === undefined) { vbox.minY = 0; }
        if (vbox.maxY === undefined) { vbox.maxY = 0; }

        // Compute map width/height and padding (relative to bbox)
        var
          w = vbox.maxX - vbox.minX,
          h = vbox.maxY - vbox.minY,
          padding = paddingRatio*Math.max(w, h);

        // Actual (x, y, w, h) values
        var
          x = vbox.minX - padding,
          y = vbox.minY - padding;
        w += 2*padding;
        h += 2*padding;

        // Update svg element
        // TODO check compatibility (jQuery/DOM)
        elem[0].setAttribute('viewBox',
          x + ' ' + y + ' ' + w + ' ' + h);
      });
    }
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
;angular.module('GHome').factory('HouseMapService', function($q, $timeout, $http) {
  var service = {};

  // Replace with an AJAX call
  service.getRooms = function() {
    var deferred = $q.defer();
    $http.get('/api/rooms').success(function(rooms) {
      deferred.resolve(rooms);
    });
    return deferred.promise;
  };
  return service;
});
;angular.module('GHome').factory('ModuleService', function($q, $http, $timeout, $upload) {
  var service = { defaultPollingDelay: 1000 },
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

  service.module = function(name) {
    var deferred = $q.defer();
    $http.get(modulesUrl + '/' + name + '/instances/status').success(function(data) {
      console.log(data);
      deferred.resolve(data);
    });
    return deferred.promise;
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
      }); // TODO handle errors
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
    httpPostJSON(storeUrl + '/rate', { name: module.id, value: value })
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

  // Poll all module instances for their statuses, passing in the module's name
  // and a callback which should be applied on a $http promise object.
  // Optionally, pass in the delay to override the service's default polling
  // delay.
  // FIXME
  service.pollInstances = function(name, callback, delay) {
    if (delay === undefined) { delay = service.defaultPollingDelay; }

    var timeout = $timeout(function pollFn() {
      callback($http.get(modulesUrl + '/' + name + '/instances/status'));
      timeout = $timeout(pollFn, delay);
    }, delay);

    return {
      cancel: function() {
        $timeout.cancel(timeout);
      }
    };
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
    httpPostJSON(modulesUrl + '/install', { name: module.id })
      .success(function() { deferred.resolve(); })
      .error(function() { deferred.reject(); });
    return deferred.promise;
  }

  return service;
});
