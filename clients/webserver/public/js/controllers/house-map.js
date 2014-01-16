function HouseMapCtrl($scope, HouseMapService) {
  // Minimal bbox used for svg display
  $scope.minX = 0;
  $scope.minY = 0;
  $scope.maxX = 0;
  $scope.maxY = 0;

  // Get the rooms (asynchronous)
  HouseMapService.getRooms().then(function(rooms) {
    $scope.rooms = rooms;
  });

  $scope.polygonPoints = function(polygon) {
    var pointsRepr = '';
    angular.forEach(polygon, function(point, i) {
      // Update min/max coordinates
      if (point.x < $scope.minX) { $scope.minX = point.x; }
      else if (point.x > $scope.maxX) { $scope.maxX = point.x; }
      if (point.y < $scope.minY) { $scope.minY = point.y; }
      else if (point.y > $scope.maxY) { $scope.maxY = point.y; }

      // Update the points representation
      pointsRepr += point.x + ',' + point.y;
      if (i < polygon.length - 1) {
        pointsRepr += ' ';
      }
    });
    return pointsRepr;
  };
}
