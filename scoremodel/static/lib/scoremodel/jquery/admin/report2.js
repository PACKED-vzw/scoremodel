/**
 * Created by pieter on 6/07/16.
 */
$(document).ready(function () {
    draw_report(get_report_data(), true);

    $('#add_section_button').click(function () {
        /* From section.js */
        add_section_button();
    });

});

function save_report_data() {
    var report_id = $('#report_id').val();
    var report_data = {
        title: $('#report_title').val(),
        lang_id: $('#report_lang').val()
    };
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
                /* Do not re-add the sections if this is a reload (saving an existing report) */
                /* Otherwise, we will have duplicates! */
                if (!is_reload) {
                    for (var i = 0; i < report.sections.length; i++) {
                        /* From section.js */
                        draw_section(get_section_data(report.sections[i].id), true);
                    }
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
            if (required_set_side_effects(['#report_title', '#report_lang'])) {
                draw_report(save_report_data(), false, true);
            }
        });
    }
}