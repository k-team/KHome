angular.module('GHome').factory('HouseMapService', function($q, $timeout) {
  var service = {};

  // Replace with an AJAX call
  service.getRooms = function() {
    var deferred = $q.defer();
    $timeout(function() {
      deferred.resolve([
        {
            "name": "Salle à manger",
            "presence": "pres_mod_1",
            "temperature": "temp_mod_1",
            "brightness": "bright_mod_1",
            "polygon": [
                { "x": 10, "y": 15 },
                { "x": 60, "y": 15 },
                { "x": 60, "y": 85 },
                { "x": 10, "y": 85 },
            ]
        }, {
            "name": "Cuisine",
            "presence": "pres_mod_2",
            "temperature": "temp_mod_2",
            "brightness": "bright_mod_2",
            "polygon": [
                { "x": 10, "y": 115 },
                { "x": 200, "y": 115 },
                { "x": 200, "y": 160 },
                { "x": 10, "y": 160 }
            ]
        }
      ]);
    }, 1000);
    console.log(deferred.promise);
    return deferred.promise;
  };
  return service;
});
