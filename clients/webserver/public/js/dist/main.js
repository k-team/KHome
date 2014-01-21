"use strict";

(function() {
  angular.module('GHome', ['ngRoute', 'angularFileUpload'])
    .config(function($routeProvider, $locationProvider) {
      $routeProvider
        .when('/home', { templateUrl: 'partials/home.html' })
        .when('/weather', { templateUrl: 'partials/weather.html' })
        .when('/surveillance', { templateUrl: 'partials/surveillance.html' })
        .when('/temperature', { templateUrl: 'partials/temperature.html' })
        .when('/brightness', { templateUrl: 'partials/brightness.html' })
        .when('/camera', { templateUrl: 'partials/camera.html' })
        .when('/power', { templateUrl: 'partials/power.html' })
        .when('/music', { templateUrl: 'partials/music.html' })
        .when('/modules', { templateUrl: 'partials/modules.html' })
        .when('/ai-config', { templateUrl: 'partials/ai-config.html' })
        .otherwise({ redirectTo: '/home' })
      ;
    });
})();
;function CatalogCtrl($scope, ModuleService) {
  // All modules
  $scope.modules = [];

  // Explicitly reload modules
  $scope.reloadModules = function() {
    ModuleService.all(function(modules) {
      console.log(modules);
      $scope.modules = modules;
    });
  };
  //...and call immediately
  $scope.reloadModules();

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
      console.error('upload failed');
    });
  };
}
;function GraphCtrl($scope, ModuleService) {
  $scope.data = [];

  var poll = ModuleService.pollStatus('t_module_1', function(promise) {
    promise.success(function(data) {
      $scope.data.push([data.time, data.temperature]);
    });
  });

  $scope.$on('$destroy', function() {
    poll.cancel();
  });
}
;function HouseMapCtrl($scope, HouseMapService) {
  // Minimal bbox used for svg display
  $scope.minX = 0;
  $scope.minY = 0;
  $scope.maxX = 0;
  $scope.maxY = 0;

  // Get the rooms (asynchronous)
  HouseMapService.getRooms().then(function(rooms) {
    $scope.rooms = rooms;
  });

  $scope.polygonPoints = function(polygon) {
    var pointsRepr = '';
    angular.forEach(polygon, function(point, i) {
      // Update min/max coordinates
      if (point.x < $scope.minX) { $scope.minX = point.x; }
      else if (point.x > $scope.maxX) { $scope.maxX = point.x; }
      if (point.y < $scope.minY) { $scope.minY = point.y; }
      else if (point.y > $scope.maxY) { $scope.maxY = point.y; }

      // Update the points representation
      pointsRepr += point.x + ',' + point.y;
      if (i < polygon.length - 1) {
        pointsRepr += ' ';
      }
    });
    return pointsRepr;
  };
}
;angular.module('GHome').directive('graph', function() {
  return {
    restrict: 'EA',
    link: function($scope, elem, attrs) {
      var chart = null, opts = {};
      $scope.$watch(attrs.graphModel, function(v) {
        console.log('graph data changed', v);
        if (!chart) {
          chart = $.plot(elem, [v], opts);
          elem.css('display', 'block');
        } else {
          chart.setData([v]);
          chart.setupGrid();
          chart.draw();
        }
      }, true);
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
;angular.module('GHome').factory('ModuleService', function($http, $timeout, $upload) {
  return {
    all: function(callback) {
      $http.get('/api/modules').success(function(data) {
        callback(data);
      });
    }, pollStatus: function(name, callback, delay) {
      if (delay === undefined) { delay = 1000; }

      var timeout = $timeout(function pollFn() {
        callback($http.get('/api/modules/' + name + '/status'));
        timeout = $timeout(pollFn, delay);
      }, delay);

      return {
        cancel: function() {
          $timeout.cancel(timeout);
        }
      };
    }, install: function(file) {
      return $upload.upload({
        url: '/api/modules/install',
        method: 'POST', file: file,
      });
    }
  };
});
