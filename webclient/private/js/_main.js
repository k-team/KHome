"use strict";

angular.module('GHome', ['ngRoute', 'ui.bootstrap', 'angularFileUpload'])
  .config(function($routeProvider, $locationProvider, $httpProvider) {
    $routeProvider.when('/home', {
      templateUrl: '/partials/home.html'
    }).when('/store', {
      templateUrl: '/partials/store.html'
    }).when('/settings', {
      templateUrl: '/partials/settings.html'
    }).when('/settings/:moduleName', {
      templateUrl: '/partials/module_settings.html'
    }).when('/modules', {
      templateUrl: '/partials/modules.html'
    }).when('/modules/:moduleName', {
      templateUrl: '/partials/module_inject.html',
      controller: 'ModuleInjectorCtrl'
    }).otherwise({
      redirectTo: '/home'
    });
  });
