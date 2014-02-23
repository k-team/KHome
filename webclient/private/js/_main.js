"use strict";

angular.module('GHome', ['ngRoute', 'ui.bootstrap', 'ui.slider', 'angularFileUpload', 'frapontillo.bootstrap-switch'])
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
