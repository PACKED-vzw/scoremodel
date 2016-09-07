/**
 * Created by pieter on 18/05/16.
 */

$(document).ready(function () {
    var scores = data_for_graph();
    var sections = sections_by_id();
    draw(scores, sections);
});

/**
 * Get a report
 * @param report_id
 * @returns {*}
 */
function get_report(report_id) {
    return $.ajax({
        method: 'GET',
        url: '/api/v2/report/' + report_id,
        contentType: 'application/json',
        success: function () {
        },
        error: function (jqXHR, status, error) {
            console.log(error);
        }
    });
}

/**
 * Get the benchmarking score for this report.
 * Do this via an ajax call to /api/v2/
 * @params benchmark_report_id
 * @returns deferred
 */
function get_benchmark_score(benchmark_report_id) {
    return $.ajax({
        method: 'GET',
        url: '/api/v2/benchmark_report/' + benchmark_report_id,
        contentType: 'application/json',
        success: function () {
        },
        error: function (jqXHR, status, error) {
            console.log(error);
        }
    });
}
// met transition en toevoegingen aan de graph => make graph global
// dit in functie van draw stoppen
// order by section
function draw_benchmark(report_id, chart_data) {
    $.when(get_report(report_id)).then(function (report_api_response) {
        for (var i = 0; i <= report_api_response.data.benchmark_reports.length; i++) {
            var benchmark_report_id = report_api_response.data.benchmark_reports[i];
            $.when(get_benchmark_score(benchmark_report_id)).then(function (benchmark_api_response) {
                var axes = [];
                for (var i = 0; i < benchmark_api_response.data.benchmarks_by_section.length; i++) {
                    var section = benchmark_api_response.data.benchmarks_by_section[i];
                    var score = 0;
                    for (var j = 0; j < section.benchmarks.length; j++) {
                        var benchmark = section.benchmarks[j];
                        if (benchmark.not_in_benchmark == true) {
                            score = +0;
                        } else {
                            score = +benchmark.score;
                        }
                    }
                    axes.push({
                        axis: section.section_id,
                        value: score
                    })
                }
                chart_data.push({
                    className: benchmark_api_response.data.title,
                    axes: axes
                })
            });
        }
    });
}

/**
 * Fetch the data from the DOM to create the graph.
 * All scores are in <span class="score" id="section_section.id">.
 * Returns an object with section.id as key and the total score as value.
 * @returns {{}}
 */
function data_for_graph() {
    var scores = {};
    $('.score').each(function () {
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
    $('.sectie').each(function () {
        var section_title = $(this).html();
        var section = $(this).attr('id').split('_');
        var section_id = section[1];
        sections[section_id] = section_title;
    });
    return sections;
}

/**
 * Draw the chart
 * https://github.com/alangrafu/radar-chart-d3
 * @param scores
 * @param sections
 */
function draw(scores, sections) {

    var chart_data = [];

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

    var c_Graph = new Graph();
    c_Graph.add_data('Resultaten', result.axes);

    c_Graph.update();
}