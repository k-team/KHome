angular.module('GHome').directive('customInput', function() {
  return {
    restrict: 'EA',
    link: function($scope, elem, attrs) {
      $scope.$watch('field.state', function(state) {
        elem.children().fadeOut(500, function() {
          elem.children().find('.glyphicon-pencil').fadeIn(500);
          console.log(elem.children().find('.glyphicon-pencil'));
        });
      });
    }
  };
});
