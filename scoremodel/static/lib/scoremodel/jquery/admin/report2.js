/**
 * Created by pieter on 6/07/16.
 */
$(document).ready(function(){
    draw_report(get_report_data(), true);
});

function save_report_data() {}

function get_report_data() {
    var report_id = $('#report_id').val();
    return $.ajax({
        method: 'GET',
        url: '/api/v2/report/' + report_id,
        success: function(data, status) {},
        error: function(jqXHR, status, error) {
            error_button('#report_save_button', error);
        }
    });
}

function draw_report(deferred, is_first_time) {
    if (deferred) {
        $.when(deferred).then(function success(report_api_response) {

        },
        function error() {})
    }
    if (is_first_time) {
        /* Register change handlers */
        var fields = ['report_title', 'report_lang'];
        for (var i = 0; i < fields.length; i++) {
            $('#' + fields[i]).focus(function() {
                default_button('#report_save_button', 'Save');
            });
        }
        /* Add click handler */
        $('#report_save_button').click(function(){
            if (required_set_side_effects(['#report_title', '#report_lang'])) {
                draw_report(save_report_data());
            }
        });
    }
}