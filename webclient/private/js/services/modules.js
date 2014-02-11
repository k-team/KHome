angular.module('GHome').factory('ModuleService', function($q, $http, $timeout, $upload) {
  var service = { defaultPollingDelay: 1000 },
    modulesUrl = '/api/modules',
    storeUrl = 'http://0.0.0.0:8889/api/available_modules';

  var getModules = function(url, cachedModules, forceReload) {
    var deferred = $q.defer();
    if (!forceReload) {
      $http.get(url).success(function(data) {
        cachedModules = data;
        deferred.resolve(data);
      }); // TODO handle errors
    } else {
      deferred.resolve(cachedModules);
    }
    return deferred.promise;
  };

  // Get the list of available modules, optionally passing if this should force
  // a reload of this list
  service.availableModules = [];
  service.available = function(forceReload) {
    return getModules(storeUrl, this.availableModules, forceReload);
  };

  service.rateModule = function(module, value) {
    var deferred = $q.defer();
    $http.post(storeUrl + '/' + module.id + '/rate', { value: value })
      .success(function() { deferred.resolve(); })
      .error(function() { deferred.reject(); });
    return deferred.promise;
  };

  // Get the list of installed modules, optionally passing if this should force
  // a reload of this list
  service.installedModules = [];
  service.installed = function(forceReload) {
    return getModules(modulesUrl, this.installedModules, forceReload);
  };

  // Poll all module instances for their statuses, passing in the module's name
  // and a callback which should be applied on a $http promise object.
  // Optionally, pass in the delay to override the service's default polling
  // delay.
  // FIXME
  service.pollInstances = function(name, callback, delay) {
    if (delay === undefined) { delay = service.defaultPollingDelay; }

    var timeout = $timeout(function pollFn() {
      callback($http.get(modulesUrl + '/' + name + '/instances/status'));
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
      url: modulesUrl + '/install',
      method: 'POST', file: file
    });
  }

  return service;
});
