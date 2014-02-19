angular.module('GHome').directive('graph', function() {
  return {
    restrict: 'EA',
    link: function($scope, elem, attrs) {
      var color_r = (Math.random()*(200)|0).toString();
      var color_g = (Math.random()*(200)|0).toString();
      var color_b = (Math.random()*(200)|0).toString();

      var chart = null, opts = {
        xaxis: {
          tickLength: 0
        }, yaxis: {
          tickLength: 0
        }, grid: {
          borderWidth: 0,
          aboveData: true,
          markings: [ { yaxis: { from: 0, to: 0 }, color: '#888' },
                      { xaxis: { from: 0, to: 0 }, color: '#888' }]
        }, series: {
          color: "rgb(" + color_r + ", " + color_g + ", " + color_b + ")",
          shadowSize: 0,
          points: {
            show: true
          }, lines: {
            show: true,
            fill: 1.0,
            fillColor: "rgba(" + color_r + ", " + color_g + ", " + color_b + ", 0.25)"
          }
        }
      };
      console.log(opts)

      // Actual plotting based on the graph data model
      $scope.$watch(attrs.graphModel, function(data) {
        var plottedData = [];
        if (data instanceof Array) {
          plottedData = data;
        } else {
          angular.forEach(data, function(rawData, label) {
            plottedData.push({ label: label, data: rawData });
          });
        }

        if (!chart) {
          chart = $.plot(elem, plottedData, opts);
          elem.css('display', 'block');
        } else {
          chart.setData(plottedData);
          chart.setupGrid();
          chart.draw();
        }
      }, true);
    }
  };
});
