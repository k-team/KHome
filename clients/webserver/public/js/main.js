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
