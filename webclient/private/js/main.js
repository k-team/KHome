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

    // LESS configuration
    less.logLevel = 1;

    // Refresh LESS when changing views (but not on first load)
    var isFirstLoad = true;
    $httpProvider.interceptors.push(function($timeout) {
      return {
        response: function(response) {
          if (isFirstLoad) { // First load, do nothing
            isFirstLoad = false;
          } else { // Refresh all LESS stylesheets
            var sheets = [], links = document.getElementsByTagName('link');
            angular.forEach(links, function(link) {
              if (link.rel == 'stylesheet/less') {
                sheets.push(link);
              }
            });

            // Check if the sheets should be refreshed
            if (less.sheets.length != sheets.length && less.sheets != sheets) {
              less.sheets = sheets;
              less.refresh();
            }
          }
          return response;
        }
      };
    });
  });
