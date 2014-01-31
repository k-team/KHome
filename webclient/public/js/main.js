"use strict";

angular.module('GHome', ['ngRoute', 'ui.bootstrap', 'angularFileUpload'])
  .config(function($routeProvider, $locationProvider, $httpProvider) {
    $routeProvider.when('/home', {
      templateUrl: '/partials/home.html'
    }).when('/store', {
      templateUrl: '/partials/store.html'
    }).when('/settings', {
      templateUrl: '/partials/settings.html'
    }).when('/modules', {
      templateUrl: '/partials/modules.html'
    }).when('/modules/:moduleName', {
      controller: 'ModuleInjectorCtrl',
      templateUrl: '/partials/module_inject.html'
    }).otherwise({
      redirectTo: '/home'
    });

    // Refresh LESS when changing views
    $httpProvider.interceptors.push(function($timeout) {
      return {
        response: function(response) {
          less.sheets = [];
          var links = document.getElementsByTagName('link');
          angular.forEach(links, function(link) {
            if (link.rel == 'stylesheet/less') {
              less.sheets.push(link);
            }
          });
          less.refresh();
          return response;
        }
      };
    });
  });
