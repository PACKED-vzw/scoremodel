/**
 * Created by pieter on 7/09/16.
 */
var graph = new Graph();
$(document).ready(function () {
    graph.init();
    /*
    We need to get a list of sections first so we can initialise the graph.
    If a benchmark or user_report has fewer sections, we pad it with section_id: 0
     */

        draw_user_report(user_report_id);
        draw_report_benchmark(report_id);
});

function draw_user_report(user_report_id) {
    var deferred = $.ajax({
        method: 'GET',
        url: '/api/v2/user_report/' + user_report_id,
        contentType: 'application/json',
        success: function () {
        },
        error: function (jqXHR, status, error) {
            console.log(error);
        }
    });
    $.when(deferred).then(function(data) {
        var title = data.data.name;
        var sections = data.data.question_answers_by_section;
        var axes = [];
        for (var i = 0; i < sections.length; i++) {
            var section = sections[i];
            var section_score = 0;
            for (var j = 0; j < section.question_answers.length; j++) {
                var question_answer = section.question_answers[j];
                section_score = section_score + (question_answer.score * question_answer.multiplication_factor);
            }
            axes.push({
                axis: section.section_id,
                value: section_score
            });
        }
        /* Redraw the graph */
        graph.add_data(title, axes);
        graph.update();
    });
}

function draw_report_benchmark(report_id) {
    var deferred = $.ajax({
        method: 'GET',
        url: '/api/v2/report/' + report_id,
        contentType: 'application/json',
        success: function () {
        },
        error: function (jqXHR, status, error) {
            console.log(error);
        }
    });
    $.when(deferred).then(function(data){
        var benchmark_reports = data.data.benchmark_reports;
        for (var i = 0; i < benchmark_reports.length; i++) {
            var r_deferred = $.ajax({
                method: 'GET',
                url: '/api/v2/benchmark_report/' + benchmark_reports[i],
                contentType: 'application/json',
                success: function () {
                },
                error: function (jqXHR, status, error) {
                    console.log(error);
                }
            });
            $.when(r_deferred).then(function(data){
                var sections = data.data.benchmarks_by_section;
                var title = data.data.title;
                var axes = [];
                for (var j = 0; j < sections.length; j++) {
                    var section = sections[j];
                    var section_score = 0;
                    for (var k = 0; k < section.benchmarks.length; k++) {
                        var benchmark = section.benchmarks[k];
                        if (benchmark.not_in_benchmark == false) {
                            section_score = section_score + (benchmark.score * benchmark.multiplication_factor);
                        }
                    }
                    axes.push({
                        axis: section.section_id,
                        value: section_score
                    });
                }
                /* Redraw the graph */
                graph.add_data('Benchmark: ' + title, axes);
                graph.update();
            })
        }
    });
}