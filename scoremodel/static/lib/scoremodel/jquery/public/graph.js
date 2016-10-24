/**
 * Created by pieter on 7/09/16.
 */

function Graph() {
    this.data = [];
}

Graph.prototype.init = function() {
    this.svg = d3.select('#graph').append('svg')
        .attr('width', 600)
        .attr('height', 600);
    this.graph = this.svg.append('g').classed('focus', 1);
    this.chart = RadarChart.chart();
    this.chart.config({
        minValue: 0,
        maxValue: 100
    });
};

Graph.prototype.add_data = function(className, axes) {
    this.data.push({
        className: className,
        axes: axes
    });
};

/**
 * Create a point for the array that goes in this.data.axes
 * @param key
 * @param value
 * @returns {{axis: *, value: *}}
 */
Graph.prototype.create_point = function(key, value) {
    return {
        axis: key,
        value: value
    }
};

/**
 Redraw the graph
 ! TODO: problem that it takes the amount of axes from the first submitted data, not the maximal amount
 */
Graph.prototype.update = function() {
    if (typeof(this.graph) == 'undefined') {
        this.init();
    }
    this.graph.datum(this.data).call(this.chart);
};