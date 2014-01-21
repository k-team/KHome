angular.module('GHome').factory('ModuleService', function($http, $timeout, $upload) {
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
