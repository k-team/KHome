"use strict";

angular.module('GHome', ['ngRoute', 'angularFileUpload'])
  .config(function($routeProvider, $locationProvider) {
    $routeProvider.when('/home', {
      templateUrl: '/partials/home.html'
    }).when('/store', {
      templateUrl: '/partials/store.html'
    }).when('/settings', {
      templateUrl: '/partials/settings.html'
    }).when('/modules', {
      templateUrl: '/partials/modules.html'
    }).when('/modules/:module_name', {
      controller: 'ModuleInjectorCtrl',
      templateUrl: '/partials/blank_module.html'
    }).otherwise({
      redirectTo: '/home'
    });
  });
