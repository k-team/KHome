function RoomsCtrl($scope) {
  // Minimal bbox af all rooms
  $scope.box = {};

  // Comma-separated representation for points (x1,y1 x2,y2 x3,y3 etc...), used
  // for svg rendering.
  $scope.points = function(room) {
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
    angular.forEach($scope.rooms, function(room) {
      angular.forEach(room.polygon, function(point) {
        if      ($scope.box.minX === undefined || point.x < $scope.box.minX) { $scope.box.minX = point.x; }
        else if ($scope.box.maxX === undefined || point.x > $scope.box.maxX) { $scope.box.maxX = point.x; }
        if      ($scope.box.minY === undefined || point.y < $scope.box.minY) { $scope.box.minY = point.y; }
        else if ($scope.box.maxY === undefined || point.y > $scope.box.maxY) { $scope.box.maxY = point.y; }
      });
    });
  });
}
