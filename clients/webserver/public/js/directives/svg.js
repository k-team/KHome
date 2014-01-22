angular.module('GHome').directive('svgVbox', function() {
  return {
    link: function($scope, elem, attrs) {
      // Configurable viewBox padding
      var padding = 0
      attrs.$observe('svgVboxPadding', function(value) {
        if (value === undefined) { return; }
        value = parseFloat($scope.$eval(value));
        padding = value;
      });

      $scope.$watch(attrs.svgVbox, function(vbox) {
        // Default values for viewBox
        if (vbox.minX === undefined) { vbox.minX = 0; }
        if (vbox.maxX === undefined) { vbox.maxX = 0; }
        if (vbox.minY === undefined) { vbox.minY = 0; }
        if (vbox.maxY === undefined) { vbox.maxY = 0; }

        // Actual (x, y, w, h) values
        var
          x = vbox.minX - padding,
          y = vbox.minY - padding,
          w = (vbox.maxX - vbox.minX) + padding,
          h = (vbox.maxY - vbox.minY) + padding;

        // Update svg element
        // TODO check compatibility (jQuery/DOM)
        elem[0].setAttribute('viewBox',
          x + ' ' + y + ' ' + w + ' ' + h);
      });
    }
  };
});
