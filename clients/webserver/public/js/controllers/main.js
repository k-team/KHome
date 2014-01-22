function MainCtrl($scope, ModuleService, HouseMapService) {
  // Module supervision (history)
  $scope.supervision = {};
  $scope.supervision.module = '';
  $scope.supervision.data = {};
  $scope.supervision.graphData = [];
  $scope.supervision.poll = null;

  $scope.$watch('supervision.module', function() {
    // Cancel the previous poll
    if ($scope.supervision.poll) {
      $scope.supervision.poll.cancel();
      $scope.supervision.data = {};
    }

    // Do nothing if the module isn't set
    if (!$scope.supervision.module) { return; }

    // Poll the current supervised module for its status, 
    $scope.supervision.poll = ModuleService.pollInstances($scope.supervision.module, function(promise) {
      promise.success(function(data) {
        angular.forEach(data, function(instance) {
          // Empty data case
          var instanceName = instance.name;
          if (!$scope.supervision.data[instanceName]) {
            $scope.supervision.data[instanceName] = [];
          }

          // Push new data
          var data = instance.data;
          $scope.supervision.data[instanceName].push([data.time, data.value]);
        });

        // Update graph-specific data
        $scope.supervision.graphData = [];
        angular.forEach($scope.supervision.data, function(data) {
          $scope.supervision.graphData.push(data);
        });
      }).error(function() {
        // TODO
      });
    });

    // Stop polling when location is changed
    $scope.$on('$routeChangeSuccess', function () {
      $scope.supervision.poll.cancel();
      $scope.supervision.module = '';
      $scope.supervision.data = {};
      $scope.supervision.graphData = [];
    });
  });

  // Get the rooms (asynchronous)
  HouseMapService.getRooms().then(function(rooms) {
    $scope.rooms = rooms;
  });

  // House map namespace
  $scope.map = {};
  // Minimal bbox af all rooms
  $scope.map.box = { minX: 0, minY: 0, maxX: 0, maxY: 0 };
  // Comma-separated representation for points (x1,y1 x2,y2 x3,y3 etc...), used
  // for svg rendering.
  $scope.map.points = function(room) {
    var pointsRepr = '';
    angular.forEach(room.polygon, function(point, i) {
      // Update the points representation
      pointsRepr += point.x + ',' + point.y;
      if (i < room.polygon.length - 1) {
        pointsRepr += ' ';
      }
    });
    return pointsRepr;
  };

  // Watch expression on rooms in order to update the bbox accordingly
  $scope.$watch('rooms', function() {
    // Compute new bbox
    angular.forEach($scope.rooms, function(room) {
      angular.forEach(room.polygon, function(point) {
        if (point.x < $scope.map.box.minX)      { $scope.map.box.minX = point.x; }
        else if (point.x > $scope.map.box.maxX) { $scope.map.box.maxX = point.x; }
        if (point.y < $scope.map.box.minY)      { $scope.map.box.minY = point.y; }
        else if (point.y > $scope.map.box.maxY) { $scope.map.box.maxY = point.y; }
      });
    });
  });
}
