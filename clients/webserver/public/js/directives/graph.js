angular.module('GHome').directive('graph', function() {
  return {
    restrict: 'EA',
    link: function($scope, elem, attrs) {
      var chart = null, opts = {};
      $scope.$watch(attrs.graphModel, function(v) {
        if (!chart) {
          chart = $.plot(elem, v, opts);
          elem.css('display', 'block');
        } else {
          chart.setData(v);
          chart.setupGrid();
          chart.draw();
        }
      }, true);
    }
  };
  });
