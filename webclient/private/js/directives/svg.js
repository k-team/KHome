angular.module('GHome').directive('svgVbox', function() {
  return {
    link: function($scope, elem, attrs) {
      // Configurable viewBox padding
      var paddingRatio = 0.05;
      attrs.$observe('svgVboxPadding', function(value) {
        if (value === undefined) { return; }
        paddingRatio = parseFloat($scope.$eval(value));
      });

      $scope.$watch(attrs.svgVbox, function(vbox) {
        // Default values for viewBox
        if (vbox.minX === undefined) { vbox.minX = 0; }
        if (vbox.maxX === undefined) { vbox.maxX = 0; }
        if (vbox.minY === undefined) { vbox.minY = 0; }
        if (vbox.maxY === undefined) { vbox.maxY = 0; }

        // Compute map width/height and padding (relative to bbox)
        var
          w = vbox.maxX - vbox.minX,
          h = vbox.maxY - vbox.minY,
          padding = paddingRatio*Math.max(w, h);

        // Actual (x, y, w, h) values
        var
          x = vbox.minX - padding,
          y = vbox.minY - padding;
        w += 2*padding;
        h += 2*padding;

        // Update svg element
        // TODO check compatibility (jQuery/DOM)
        elem[0].setAttribute('viewBox',
          x + ' ' + y + ' ' + w + ' ' + h);
      });
    }
  };
});
