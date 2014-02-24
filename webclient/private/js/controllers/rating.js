function RatingCtrl($scope, ModuleService) {
  $scope.$on('module.statusUpdate', function(_, module) {
    ModuleService.getRate(module).then(function(rate) {
      module.rating = rate;
    });
  });

  $scope.isRating = false;
  $scope.rate = function() {
    $scope.ratingOk = false;
    $scope.isRating = true;
    ModuleService.setRate($scope.module, $scope.module.rating).then(function() {
      $scope.ratingOk = true;
      $scope.isRating = false;
    }, function() {
      $scope.isRating = false;
    });
  };
}
