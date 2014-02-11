"use strict";

angular.module('GHome', ['ngRoute', 'ui.bootstrap', 'angularFileUpload'])
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

  // Module supervision (history)
  $scope.supervision = {};
  $scope.supervision.module = '';
  $scope.supervision.data = {};
  $scope.supervision.maxData = 10;
  $scope.supervision.poll = null;

  $scope.$watch('supervision.module', function() {
    // Cancel the previous poll
    if ($scope.supervision.poll) {
      $scope.supervision.poll.cancel();
      $scope.supervision.data = {};
    }

    // Do nothing if the module isn't set
    if (!$scope.supervision.module) { return; }

    // Poll the current supervised module for its status
    $scope.supervision.poll = ModuleService.pollInstances($scope.supervision.module, function(promise) {
      promise.success(function(data) {
        angular.forEach(data, function(instance) {
          var instanceName = instance.name;
          angular.forEach(instance.attrs, function(data, attr) {
            var attrName = instanceName + '.' + attr
            // Empty data case
            if (!$scope.supervision.data[attrName]) {
              $scope.supervision.data[attrName] = [];
            }

            // Push new data
            var attrData = $scope.supervision.data[attrName];
            attrData.push([instance.time, data]);
            if ($scope.supervision.maxData < attrData.length) {
              attrData.splice(0, attrData.length - $scope.supervision.maxData);
            }
          });
        });
      }).error(function() {
        // TODO
      });
    });

    // Stop polling when location is changed
    $scope.$on('$routeChangeSuccess', function () {
      $scope.supervision.poll.cancel();
      $scope.supervision.module = '';
      $scope.supervision.data = {};
      $scope.supervision.graphData = [];
    });
  });

  // Get the rooms (asynchronous)
  HouseMapService.getRooms().then(function(rooms) {
    $scope.rooms = rooms;
  });

  // House map namespace
  $scope.map = {};

  // Minimal bbox af all rooms
  $scope.map.box = {};

  // Comma-separated representation for points (x1,y1 x2,y2 x3,y3 etc...), used
  // for svg rendering.
  $scope.map.points = function(room) {
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

  // Compute map padding (relative to bbox)
  $scope.map.padding = function() {
    return $scope.map.paddingRatio*Math.max(
        $scope.map.box.maxX - $scope.map.box.minX,
        $scope.map.box.maxY - $scope.map.box.minY);
  };
  // padding = ratio*max(width, height)
  $scope.map.paddingRatio = 0.05;

  // Watch expression on rooms in order to update the bbox accordingly
  $scope.$watch('rooms', function() {
    angular.forEach($scope.rooms, function(room) {
      angular.forEach(room.polygon, function(point) {
        if      ($scope.map.box.minX === undefined || point.x < $scope.map.box.minX) { $scope.map.box.minX = point.x; }
        else if ($scope.map.box.maxX === undefined || point.x > $scope.map.box.maxX) { $scope.map.box.maxX = point.x; }
        if      ($scope.map.box.minY === undefined || point.y < $scope.map.box.minY) { $scope.map.box.minY = point.y; }
        else if ($scope.map.box.maxY === undefined || point.y > $scope.map.box.maxY) { $scope.map.box.maxY = point.y; }
      });
    });
  });
}
;function ModuleInjectorCtrl($scope, $routeParams, $compile, $http) {
  $scope.moduleName = $routeParams.moduleName;
  $scope.templateUrl = '/api/modules/' + $scope.moduleName
    + '/public/partial.html';

  $http.get($scope.templateUrl).then(function(result){
    console.log(result.data);
    $scope.moduleContent = result.data;

    // Note: this is a hack, but it works
    $('#inject').html($compile(result.data)($scope));
  });
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
    $location.path(module.has_view ? '/modules/' + module.id : '/settings');
  };
}
;function SettingsCtrl($scope, $location) {
  $scope.reloadModules();

  $scope.navigate = function(module) {
    $location.path('/settings/' + module.id);
  };
}
;function RatingCtrl($scope) {
  $scope.setRating = function(module, value) {
    console.log('Motherfucker')
  };
}

function StoreCtrl($scope, $modal, ModuleService) {
  // All modules
  $scope.modules = [];

  // Explicitly reload modules
  $scope.reloadModules = function() {
    ModuleService.available().then(function(modules) {
      $scope.modules = modules;
    });
  };
  //...and call immediately
  $scope.reloadModules();

  // Install a module
  $scope.install = function(module) {
    console.log('installing module', module);
  };

  // Uploading system
  $scope.uploading = false
  $scope.upload = function(file) {
    $scope.uploading = true;
    $scope.upload = ModuleService.install(file).progress(function(evt) {
      $scope.uploadProgress = parseInt(100.0 * evt.loaded / evt.total);
    }).success(function() {
      $scope.uploading = false;
      $scope.reloadModules();
    }).error(function() {
      $scope.uploading = false;
      // TODO handle errors better
    });
  };

  $scope.ratingCtrl = function($scope) {
    $scope.hoveringOver = function(value) {
      $scope.overStar = value;
      $scope.percent = 100 * (value / $scope.max);
    };

    $scope.ratingStates = [
    {stateOn: 'glyphicon-ok-sign', stateOff: 'glyphicon-ok-circle'},
    {stateOn: 'glyphicon-star', stateOff: 'glyphicon-star-empty'},
    {stateOn: 'glyphicon-heart', stateOff: 'glyphicon-ban-circle'},
    {stateOn: 'glyphicon-heart'},
    {stateOff: 'glyphicon-off'}
    ];
  }

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
;angular.module('GHome').directive('svgVbox', function() {
  return {
    link: function($scope, elem, attrs) {
      // Configurable viewBox padding
      var padding = 0
      attrs.$observe('svgVboxPadding', function(value) {
        if (value === undefined) { return; }
        value = parseFloat($scope.$eval(value));
        padding = value;
      });

      $scope.$watch(attrs.svgVbox, function(vbox) {
        // Default values for viewBox
        if (vbox.minX === undefined) { vbox.minX = 0; }
        if (vbox.maxX === undefined) { vbox.maxX = 0; }
        if (vbox.minY === undefined) { vbox.minY = 0; }
        if (vbox.maxY === undefined) { vbox.maxY = 0; }

        // Actual (x, y, w, h) values
        var
          x = vbox.minX - padding,
          y = vbox.minY - padding,
          w = (vbox.maxX - vbox.minX) + 2*padding,
          h = (vbox.maxY - vbox.minY) + 2*padding;

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
    storeUrl = 'http://0.0.0.0:8889';

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
    return getModules(storeUrl + '/api/available_modules',
        this.availableModules, forceReload);
  };

  // Get the list of installed modules, optionally passing if this should force
  // a reload of this list
  service.installedModules = [];
  service.installed = function(forceReload) {
    return getModules('/api/modules', this.installedModules, forceReload);
  };

  // Poll all module instances for their statuses, passing in the module's name
  // and a callback which should be applied on a $http promise object.
  // Optionally, pass in the delay to override the service's default polling
  // delay.
  // FIXME
  service.pollInstances = function(name, callback, delay) {
    if (delay === undefined) { delay = service.defaultPollingDelay; }

    var timeout = $timeout(function pollFn() {
      callback($http.get('/api/modules/' + name + '/instances/status'));
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
  service.install = function(file) {
    return $upload.upload({
      url: '/api/modules/install',
      method: 'POST', file: file,
    });
  }

  return service;
});
