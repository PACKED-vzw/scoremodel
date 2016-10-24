/**
 * Created by pieter on 7/07/16.
 */

$(document).ready(function () {
});

function delete_section_button(section_id) {
    if (section_id < 0) {
        delete_section_data(section_id);
    } else {
        $.when(delete_section_data(section_id)).then(function () {
            $('#section_panel_' + section_id).remove();
        });
    }
}

function add_section_button() {
    var last_section_id_el = $('#last_section_id');
    var last_section_id = parseInt(last_section_id_el.val()) - 1;
    last_section_id_el.val(last_section_id);
    var section_data = {
        id: last_section_id,
        title: null,
        context: null
    };
    $('#sections').append(draw_section_template(section_data));
    add_section_focus_handlers(last_section_id);
    add_section_click_handlers(last_section_id);
}


function section_data_from_form(section_id) {
    return {
        title: $('#section_title_' + section_id).val(),
        context: $('#section_context_' + section_id).val(),
        weight: $('#section_weight_' + section_id).val(),
        report_id: $('#report_id').val(),
        id: section_id
    }
}


function get_section_data(section_id) {
    return $.ajax({
        method: 'GET',
        url: '/api/v2/section/' + section_id,
        success: function (data, status) {
        },
        error: function (jqXHR, status, error) {
            error_button('#report_save_button', error);
        }
    });
}

function draw_section(deferred, is_first_time) {
    /* Render the template */
    if (deferred) {
        $.when(deferred).then(function success(section_api_data, status, jqXHR) {
            var section = section_api_data.data;
            var sections = $('#sections');
            sections
                .find('#section_id_placeholder_' + section.id)
                .replaceWith(draw_section_template(section));
            /* Add the questions */
            var questions_dom = $('#questions_section_' + section.id);
            for (var j = 0; j < section.questions.length; j++) {
                /* From question.js */
                questions_dom.append('<div class="panel panel-default" id="question_id_placeholder_' + section.questions[j].id + '"><div class="panel-heading"><h4 class="panel-title">' + section.questions[j].question + '</h4></div></div>');
                draw_question(get_question_data(section.questions[j].id), true);
            }

            /* Add the focus and click handlers */
            if (is_first_time) {
                /* Focus */
                add_section_focus_handlers(section.id);
                add_section_click_handlers(section.id);
            }
            questions_dom.sortable({
                items: '> .question',
                cursor: 'move',
                update: function(ui, event) {
                    default_button('#report_save_button', 'Save');
                }
            });
        }, function error(jqXHR, status, error) {
            /* We can't set the error_button here, as we don't know the section_id */
        });
    }
}

/**
 * Delete a section.
 * If the section has questions, delete those as well.
 * @param section_id
 */
function delete_section_data(section_id) {
    $('#questions_section_' + section_id).find('.question').each(function () {
        var contains_id = $(this).attr('id');
        /* The value of the id attribute of div.question is like question_id */
        var id_parts = contains_id.split('_');
        delete_question_data(id_parts[id_parts.length - 1]);
    });
    /* If section_id < 0, simple remove it from the DOM (it was not saved) */
    if (section_id < 0) {
        $('#section_panel_' + section_id).remove();
    } else {
        return $.ajax({
            method: 'DELETE',
            url: '/api/v2/section/' + section_id,
            success: function () {
            },
            error: function (jqXHR, status, error) {
                error_button('#section_' + section_id + '_remove_button', error);
            }
        });
    }
}

function add_section_focus_handlers(section_id) {
    var fields = ['section_title_' + section_id, 'section_context_' + section_id, 'section_weight_' + section_id];
    for (var i = 0; i < fields.length; i++) {
        $('#' + fields[i]).focus(function () {
            default_button('#report_save_button', 'Save');
        });
    }
}

function add_section_click_handlers(section_id) {
    $('#section_' + section_id + '_remove_button').click(function () {
        delete_section_button(section_id);
    });
    $('#add_question_button_section_' + section_id).click(function () {
        /* From question.js */
        add_question_button(section_id);
    });
}

/**
 * Given the object section_data (containing section_data.id, section_data.title, section_data.context),
 * render the jquery template #section_template with section_data as a parameter.
 * @param section_data
 */
function draw_section_template(section_data) {
    var section_template = $.templates('#section-template');
    var template_data = {
        section_id: section_data.id,
        section_title: section_data.title,
        section_context: section_data.context,
        section_weight: section_data.weight
    };
    return section_template.render(template_data);
}

function required_check_section(section_id) {
    var required = ['#section_title_' + section_id, '#section_weight_' + section_id];
    return required_set_side_effects(required);
}