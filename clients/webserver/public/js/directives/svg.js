angular.module('GHome').directive('svgVbox', function() {
  return {
    link: function($scope, elem, attrs) {
      $scope.$watch(attrs.svgVbox, function(vbox) {
        console.log('svgVbox value changed');
        elem[0].setAttribute('viewBox',
          vbox.minX + ' ' +
          vbox.minY + ' ' +
          (vbox.maxX - vbox.minX) + ' ' +
          (vbox.maxY - vbox.minY) + ' '
         );
      });
    }
  };
});
