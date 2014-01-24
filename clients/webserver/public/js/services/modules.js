angular.module('GHome').factory('ModuleService', function($q, $http, $timeout, $upload) {
  var service = {
    defaultPollingDelay: 1000
  };

  service.modules = [];

  // Get the list of available modules, optionally passing if this should force
  // a reload of this list
  service.all = function(forceReload) {
    var deferred = $q.defer();
    if (!forceReload) {
      $http.get('/api/modules').success(function(data) {
        service.modules = data;
        deferred.resolve(data);
      }); // TODO handle errors
    } else {
      deferred.resolve(this.modules);
    }
    return deferred.promise;
  };

  // Poll all module instances for their statuses, passing in the module's name
  // and a callback which should be applied on a $http promise object.
  // Optionally, pass in the delay to override the service's default polling
  // delay.
  // FIXME
  service.pollInstances = function(name, callback, delay) {
    if (delay === undefined) { delay = service.defaultPollingDelay; }

    var timeout = $timeout(function pollFn() {
      callback($http.get('/api/modules/' + name + '/instances/status'));
      timeout = $timeout(pollFn, delay);
    }, delay);

    return {
      cancel: function() {
        $timeout.cancel(timeout);
      }
    };
  };

  // Install a module, passing in the uploaded file object (see $upload for
  // details). Return a promise object for the given upload http call.
  service.install = function(file) {
    return $upload.upload({
      url: '/api/modules/install',
      method: 'POST', file: file,
    });
  }

  return service;
});
