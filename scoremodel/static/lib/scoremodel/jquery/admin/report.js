/**
 * Created by pieter on 23/05/16.
 */


$(document).ready(function(){
    /*
    All templates are already part of edit.hml, with the id #section-template and #question-template.
    They are hidden at the end of the edit page.
     */
    var sections = [];
    var report_id = $('#report_id').attr('value');
    /*
    Get all sections: a section contains all of its questions and answers.
     */
    $.ajax({
        method: 'GET',
        url: '/api/v2/report/' + report_id,
        success: function(data, status) {
            for(var i = 0; i < data.data.sections.length; i++) {
                var section = data.data.sections[i];
                add_section(section);
            }
        },
        error: function(jqXHR, status, error) {}
    });
    /*
    Save buttons
     */
    $('#report_save_button').find('button').click(function(){
        save_report(report_id);
    });
    /*
    Add new section button
     */
    $('#add_section_button').click(function(){
        new_section();
    });
    
});

function save_report(report_id) {
    var report_data = {
        title: $('#report_title').val(),
        lang_id: $('#report_lang').val()
    };
    $.ajax({
        method: 'PUT', /* Reports are always PUT, the exist before we get to this part of the application */
        url: '/api/v2/report/' + report_id,
        data: JSON.stringify(report_data),
        success: function(data, status) {
            /* Update report_title with information from the DB. Set the button. */
            $('#report_title')
                .attr('value', data.data.title)
                .change(function() {
                    /* Reset the 'Save' button if the contents of this field changes */
                    $('#report_save_button')
                        .find('button').click(function () {
                        save_report(report_id);
                    });
                    default_button('#report_save_button', 'Save');
                });
            success_button('#report_save_button', 'Saved');
        },
        error: function(jqXHR, status, error) {
            error_button('#report_save_button', error);
        }
    });
}
