angular.module('GHome').factory('ModulePolling', function($http, $timeout) {
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
