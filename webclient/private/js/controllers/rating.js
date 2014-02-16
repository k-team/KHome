function RatingCtrl($scope, ModuleService) {
  $scope.isRating = false;
  $scope.rate = function() {
    $scope.isRating = true;
    ModuleService.rate($scope.module, $scope.module.rating).then(function() {
      console.log('rating success');
    }, function() {
      console.log('rating error');
    }, function() {
      $scope.isRating = false;
    });
  };
}
