/**
 * Created by pieter on 7/07/16.
 */

function delete_section_button(section_id) {
    if (section_id < 0) {
        delete_section_data(section_id);
    } else {
        $.when(delete_section_data(section_id)).then(function() {
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

function save_section_button(section_id) {
    var report_id = $('#report_id').val();
    if (report_id < 0) {
        /* We must first save the report */
        $.when(save_report_data()).then(function success(report_data, status, jqXHR) {
            /* data.data = report */
            draw_report(jqXHR, false, true);
            draw_section(save_section_data(section_id), false, section_id);
        });
    } else {
        draw_section(save_section_data(section_id), false, section_id);
    }
}

function save_section_data(section_id) {
    var section_data = {
        title: $('#section_title_' + section_id).val(),
        context: $('#section_context_' + section_id).val(),
        report_id: $('#report_id').val()
    };
    var url;
    var method;
    if (section_id < 0) {
        url = '/api/v2/section';
        method = 'POST';
    } else {
        url = '/api/v2/section/' + section_id;
        method = 'PUT';
    }
    return $.ajax({
        method: method,
        url: url,
        data: JSON.stringify(section_data),
        success: function (data) {

        },
        error: function (jqXHR, status, error) {
            error_button('#section_' + section_id + '_save_button', error);
        }
    });
}

function get_section_data(section_id) {
    return $.ajax({
        method: 'GET',
        url: '/api/v2/section/' + section_id,
        success: function (data, status) {
        },
        error: function (jqXHR, status, error) {
            error_button('#section_' + section_id + '_save_button', error);
        }
    });
}

function draw_section(deferred, is_first_time, old_section_id) {
    /* Render the template */
    if (deferred) {
        $.when(deferred).then(function success(section_api_data, status, jqXHR) {
            var section = section_api_data.data;
            /* If old_section_id, do not append but replace */
            if (old_section_id) {
                replace_existing_section(old_section_id, section);
            } else {
                $('#sections').append(draw_section_template(section));
                /* Add the questions */
                for (var j = 0; j < section.questions.length; j++) {
                    /* From question.js */
                    draw_question(get_question_data(section.questions[j].id), true);
                }
            }
            /* Add the focus and click handlers */
            if (is_first_time) {
                /* Focus */
                add_section_focus_handlers(section.id);
                /* Click */
                add_section_click_handlers(section.id);
            }
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
    $('#questions_section_' + section_id).find('.question').each(function(){
        var contains_id = $(this).attr('id'); /* The value of the id attribute of div.question is like question_id */
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
            success: function() {},
            error: function (jqXHR, status, error) {
                error_button('#section_' + section_id + '_remove_button', error);
            }
        });
    }
}

function add_section_focus_handlers(section_id) {
    var fields = ['section_title_' + section_id, 'section_context_' + section_id];
    for (var i = 0; i < fields.length; i++) {
        $('#' + fields[i]).focus(function () {
            default_button('#section_' + section_id + '_save_button', 'Save');
            default_button('#section_' + section_id + '_remove_button', 'Remove');
        });
    }
}

function add_section_click_handlers(section_id) {
    $('#section_' + section_id + '_save_button').click(function () {
        if (required_set_side_effects(['#section_title_' + section_id])) {
            save_section_button(section_id);
        }
    });
    $('#section_' + section_id + '_remove_button').click(function () {
        delete_section_button(section_id);
    });
    $('#add_question_button_section_' + section_id).click(function() {
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
        section_context: section_data.context
    };
    return section_template.render(template_data);
}

/**
 * Replace an existing section.
 * Redraw the template, but keep the questions
 * We could just get the questions from the API again, but
 * this might cause the work a user just has done in an
 * unsaved question to be lost.
 * We cannot simply first save the questions, as you can't
 * create a new question without an existing section_id.
 * So you wouldn't be able to create a new section with a
 * new question and save it.
 * Better options might be available
 * @param old_section_id
 * @param section_data
 */
function replace_existing_section(old_section_id, section_data) {
    var old_section = $('#section_panel_' + old_section_id);
    var questions = $('#questions_section_' + old_section_id).contents().clone(true);
    /* As you can only save a section when aria-expanded is true, we keep this setting
     to prevent panels from closing abruptly, confusing users. */
    var aria_state = old_section.find('.panel-heading').attr('aria-expanded');
    var new_section_id = section_data.id;
    old_section.replaceWith(draw_section_template(section_data));
    $('#questions_section_' + new_section_id).replaceWith(questions);
    /* Collapsed or not? */
    if (aria_state == 'true') {
        set_collapsed_state('#section_panel_' + new_section_id);
    }
    /* Focus */
    add_section_focus_handlers(new_section_id);
    /* Click */
    add_section_click_handlers(new_section_id);
    /* Success button */
    success_button('#section_' + new_section_id + '_save_button', 'Saved');
}

/**
 * When updating a question/section, the DOM of that item is re-inserted using the template.
 * This has as side-effect that the item that was opened (not collapsed) is collapsed again
 * (which is the default state). This is annoying for users.
 * @param selector
 */
function set_collapsed_state(selector) {
    $(selector)
        .find('.panel-heading')
        .attr('aria-expanded', true);
    $(selector)
        .find('.panel-body')
        .attr('aria-expanded', true)
        .addClass('collapse in');
}