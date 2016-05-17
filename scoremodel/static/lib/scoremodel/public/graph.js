var app = angular.module('scoremodel.graph', ['scoremodel.api_core', 'scoremodel.api_submit']);

app.controller('SectionCtrl', ['$scope', 'ApiCore', 'ApiSubmit',
    function($scope, ApiCore, ApiSubmit) {

        /*
        Get data
         */
        var data = [];
        
        /*
        Groen veld = certificatie DSA minimum
         */

        $scope.draw = function(){
            /* https://github.com/alangrafu/radar-chart-d3 */
            var chart = RadarChart.chart();
            var svg = d3.select('#chart').append('svg')
                .attr('width', 600)
                .attr('height', 800);
            svg.append('g').classed('focus', 1).datum($scope.data).call(chart);
        };
    }]);
