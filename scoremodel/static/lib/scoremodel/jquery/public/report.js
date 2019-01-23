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
    add_loader('#graph_loader');
    $.when(deferred).then(function(data) {
        remove_loader('#graph_loader');
        draw_user_report(data.data);
        draw_report_benchmark(data.data);
    });
});

function draw_user_report(data) {
    var title = data.name;
    var sections = data.question_answers_by_section;
    var axes = [];
    for (var i = 0; i < sections.length; i++) {
        var section = sections[i];
        var section_score = 0;
        for (var j = 0; j < section.question_answers.length; j++) {
            var question_answer = section.question_answers[j];
            section_score = section_score + (question_answer.score * question_answer.multiplication_factor);
        }
        axes.push({
            axis: section.section_title,
            value: section_score
        });
    }
    /* Redraw the graph */
    graph.add_data(title, axes);
    graph.update();
}

function draw_report_benchmark(data) {
    var sections = data.question_answers_by_section;
    var title = "DSA";
    var axes = [];
    for (var i = 0; i < sections.length; i++) {
        var section = sections[i];
        var section_score = 0;
        for (var j = 0; j < section.question_answers.length; j++) {
            var question_answer = section.question_answers[j];
            if (question_answer.not_in_benchmark == false) {
                if (question_answer.score > 0) {
                    section_score += (100 / section.benchmark_count)
                }
            }
        }
        axes.push({
            axis: section.section_id,
            value: section_score
        });
    }
    /* Redraw the graph */
    graph.add_data(_('Benchmark: ') + title, axes);
    graph.update();
}
