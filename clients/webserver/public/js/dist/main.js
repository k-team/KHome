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
;angular.module('GHome').controller('HouseMapCtrl', ['$scope', function($scope) {
  $scope.rooms = [
      {
          "name": "Salle à manger",
          "presence": "pres_mod_1",
          "temperature": "temp_mod_1",
          "brightness": "bright_mod_1",
          "polygon": [
              { "x": 10, "y": 15 },
              { "x": 61, "y": 32 },
              { "x": 42, "y": 12 },
              { "x": 13, "y": 50 },
              { "x": 50, "y": 54 }
          ]
      }, {
          "name": "Cuisine",
          "presence": "pres_mod_2",
          "temperature": "temp_mod_2",
          "brightness": "bright_mod_2",
          "polygon": [
              { "x": 79, "y": 23 },
              { "x": 28, "y": 61 },
              { "x": 70, "y": 75 },
              { "x": 47, "y": 70 },
              { "x": 72, "y": 28 }
          ]
      }
  ];

  $scope.polygonPoints = function(polygon) {
    var pointsRepr = '';
    angular.forEach(polygon, function(point, i) {
      pointsRepr += point.x + ',' + point.y;
      if (i < polygon.length - 1) {
        pointsRepr += ' ';
      }
    });
    return pointsRepr;
  };
}]);
