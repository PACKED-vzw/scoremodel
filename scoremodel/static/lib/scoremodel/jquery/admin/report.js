/**
 * Created by pieter on 6/07/16.
 */
$(document).ready(function () {

    draw_report(get_report_data(), true);

    $('#add_section_button').click(function () {
        /* From section.js */
        add_section_button();
    });

    $('#sections').sortable(
        {
            items: '> .section',
            cursor: 'move'
        }
    );

});

function report_data_from_form() {
    return {
        title: $('#report_title').val(),
        lang_id: $('#report_lang').val(),
        id: $('#report_id').val()
    };
}

function save_report_data() {
    var report_id = $('#report_id').val();
    var report_data = report_data_from_form();
    var url;
    var method;
    if (report_id < 0) {
        url = '/api/v2/report';
        method = 'POST';
    } else {
        url = '/api/v2/report/' + report_id;
        method = 'PUT';
    }
    return $.ajax({
        method: method,
        url: url,
        data: JSON.stringify(report_data),
        success: function () {
        },
        error: function (jqXHR, status, error) {
            error_button($('#report_save_button', error));
        }
    });
}

function save_report_chain() {
    /* TODO: check for required stuff */
    //required_set_side_effects(['#section_title_' + section_id])

    var required_missing = false;

    if (!required_check_report()) {
        required_missing = true;
    }

    var report = report_data_from_form();
    var report_id = $('#report_id').val();

    report.sections = [];
    var section_order = 0;
    $('#sections').children().each(function() {
        section_order = section_order + 1;
        var section_id = $(this).attr('id').substr(14);
        if (!required_check_section(section_id)) {
            required_missing = true;
        }
        var section = section_data_from_form(section_id);
        section.id = parseInt(section_id);
        section.order_in_report = section_order;
        section.questions = [];
        // Check for required fields
        var question_order = 0;
        $('#questions_section_' + section_id).children().each(function() {
            question_order = question_order + 1;
            var question_id = $(this).attr('id').substr(9);
            if (!required_check_question(question_id)) {
                required_missing = true;
            }
            var question = question_data_from_form(question_id);
            question.order_in_section = question_order;
            question.id = parseInt(question_id);
            section.questions.push(question);
        });
        report.sections.push(section);
    });

    var url;
    var method;
    if (report_id < 0) {
        url = '/api/v2/report';
        method = 'POST';
    } else {
        url = '/api/v2/report/' + report_id;
        method = 'PUT';
    }

    //var s = $('#sections').sortable('toArray');

    //console.log(s);

    if (required_missing) {
        return null;
    }

    return $.ajax({
        method: method,
        url: url,
        data: JSON.stringify(report),
        success: function () {
             success_button('#report_save_button', 'Saved');
        },
        error: function (jqXHR, status, error) {
            error_button($('#report_save_button', error));
        }
    });
}

function get_report_data() {
    var report_id = $('#report_id').val();
    return $.ajax({
        method: 'GET',
        url: '/api/v2/report/' + report_id,
        success: function (data, status) {
        },
        error: function (jqXHR, status, error) {
            error_button('#report_save_button', error);
        }
    });
}

function draw_report(deferred, is_first_time, is_reload) {
    if (deferred) {
        $.when(deferred).then(function success(report_api_response) {
                var report = report_api_response.data;
                $('#report_title').val(report.title);
                $('#report_lang').val(report.lang_id);
                /* Add sections */
                /* Remove the old sections first */
                $('#sections').children().remove();
                for (var i = 0; i < report.sections.length; i++) {
                    /* From section.js */
                    /* As we removed the old sections, it is always "the first time" */
                    draw_section(get_section_data(report.sections[i].id), true);
                }

            },
            function error(jqXHR, status, error) {
                error_button('#report_save_button', error);
            })
    }
    if (is_first_time) {
        /* Register change handlers */
        var fields = ['report_title', 'report_lang'];
        for (var i = 0; i < fields.length; i++) {
            $('#' + fields[i]).focus(function () {
                default_button('#report_save_button', 'Save');
            });
        }
        /* Add click handler */
        $('#report_save_button').click(function () {
            draw_report(save_report_chain(), false, true);
        });
    }
}

function required_check_report() {
    var required = ['#report_title', '#report_lang'];
    return required_set_side_effects(required);
}
