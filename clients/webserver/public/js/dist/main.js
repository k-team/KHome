"use strict";

(function() {
  angular.module('GHome', ['ngRoute'])
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
        .when('/module-config', { templateUrl: 'partials/module-config.html' })
        .when('/ai-config', { templateUrl: 'partials/ai-config.html' })
        .otherwise({ redirectTo: '/home' })
      ;
    });
})();
;function GraphCtrl($scope, ModulePolling) {
  $scope.data = [];

  var poll = ModulePolling.poll('t_module_1', function(promise) {
    promise.success(function(data) {
      $scope.data.push([$scope.data.length, data.temperature]);
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
;angular.module('GHome').factory('ModulePolling', function($http, $timeout) {
  return {
    poll: function(name, callback, delay) {
      if (delay === undefined) { delay = 500; }

      var timeout = $timeout(function pollFn() {
        callback($http.get('/api/modules/' + name + '/status'));
        timeout = $timeout(pollFn, delay);
      }, delay);

      return {
        cancel: function() {
          $timeout.cancel(timeout);
        }
      };
    }
  };
});
