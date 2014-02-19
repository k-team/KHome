angular.module('GHome').directive('graph', function() {
  return {
    restrict: 'EA',
    link: function($scope, elem, attrs) {
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
          color: "#"+('00000'+(Math.random()*(1<<24)|0).toString(16)).slice(-6),
          shadowSize: 0,
          points: {
            show: true
          }, lines: {
            show: true
          }
        }
      };

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
