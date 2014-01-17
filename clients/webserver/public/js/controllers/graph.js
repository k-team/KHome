function GraphCtrl($scope, $timeout) {
	$scope.data = [];
	var delay = 500;
	$timeout(function pushData() {
		console.log($scope.data.length);
		$scope.data.push([$scope.data.length, $scope.data.length*$scope.data.length]);
		$timeout(pushData, delay);
	}, delay);
}