/**
 * Created by pieter on 18/05/16.
 */

$(document).ready(function() {
    var scores = data_for_graph();
    var sections = sections_by_id();
    draw(scores, sections);
});

/**
 * Fetch the data from the DOM to create the graph.
 * All scores are in <span class="score" id="section_section.id">.
 * Returns an object with section.id as key and the total score as value.
 * @returns {{}}
 */
function data_for_graph() {
    var scores = {};
    $('.score').each(function(){
        var score = $(this).html();
        var section = $(this).attr('id').split('_');
        var section_id = section[1];
        scores[section_id] = score;
    });
    return scores;
}

/**
 * Get the title for every section by section.id
 * All section_titles are in <span class="sectie" id="section_section_id">.
 * Returns an object with section.id as key and the title as value.
 * @returns {{}}
 */
function sections_by_id() {
    var sections = {};
    $('.sectie').each(function(){
        var section_title = $(this).html();
        var section = $(this).attr('id').split('_');
        var section_id = section[1];
        sections[section_id] = section_title;
    });
    return sections;
}

/**
 * https://github.com/alangrafu/radar-chart-d3
 * @param scores
 * @param sections
 */
function draw(scores, sections) {

    var data = [
    ];

    var benchmark = {
        className: 'benchmark',
        axes: []
    };
    var result = {
        className: 'Resultaten',
        axes: []
    };

    for (var section_id in sections) {
        if (sections.hasOwnProperty(section_id)) {
            result.axes.push({
                axis: sections.section_id,
                value: scores[section_id]
            });
            /* TODO: add benchmark (via API call) */
        }
    }

    data.push(result);


    var chart = RadarChart.chart();

    chart.config({
        minValue: 0,
        maxValue: 100
    });

    /*var data = [
  {
    className: 'germany', // optional can be used for styling
    axes: [
      {axis: "strength", value: 13, yOffset: 10},
      {axis: "intelligence", value: 6},
      {axis: "charisma", value: 5},
      {axis: "dexterity", value: 9},
      {axis: "luck", value: 2, xOffset: -20}
    ]
  }*/

    var svg = d3.select('#graph').append('svg')
      .attr('width', 600)
      .attr('height', 600);
    svg.append('g').classed('focus', 1).datum(data).call(chart);
}