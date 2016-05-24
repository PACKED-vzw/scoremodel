// TODO: change handler on all input fields

$(document).ready(function () {

});

var section_data_fields = ['title', 'context'];

/**
 * Create a new section that has not yet been submitted to the database. We submit sections to the DB when
 *  - a user clicks "Save"
 *  - a user adds a question
 *  - a user saves a question in a new section
 * New, uncommitted sections always have an id < 0.
 */
function new_section() {
    /* We must have an unique id, which should be a < 0, because the application has no
     ids < 0. To make sure we don't use two times the same id, we get and set it form
     input.id = last_section_id. We get the value and substract 1.
     When a section is committed to the database, its id changes to the one it
     received in the DB */
    var last_id = $('#last_section_id').attr('value');
    /* .title and .context must be present, but must have a null value so this script defaults
     to the strings provided by flask/jinja, which are translated */
    var section = {
        id: last_id - 1,
        title: null,
        context: null,
        questions: []
    };
    $('#last_section_id').attr('value', last_id - 1);
    return add_section(section);
}

/**
 * From a section object, add a new section to the DOM.
 *  - Get the template (using jsrender) called '#section-template' (part of the DOM already, but hidden)
 *  - Fill in section_id, section_title and section_context
 *  - Render it
 *  - Append it to #sections
 * @param section
 */
function add_section(section) {
    var section_template = $.templates('#section-template');
    var template_vars = {
        section_id: section.id,
        section_title: section.title,
        section_context: section.context
    };
    $('#sections').append(section_template.render(template_vars));
    /* Add questions */
    for (var i = 0; i < section.questions.length; i++) {
        var question = section.questions[i];
        add_question(question, section.id);
    }
    /* Add .click-callback to the save button */
    $('#section_' + section.id + '_save_button').find('button')
        .click(function () {
            save_section(section.id);
        });
    $('#section_' + section.id + '_remove_button').find('button')
        .click(function () {
            delete_section(section.id);
        });
    /*
     Add new question button
     */
    $('#add_question_button_section_' + section.id).click(function () {
        new_question(section.id);
    });
    return true;
}

/**
 * Save the current section.
 *  - Store the current section (store_section)
 *  - Store all dependent questions (store_question)
 *  - Redraw the dependent questions (redraw_question)
 *  - Redraw the current section (redraw_section)
 *
 *  We must store all dependent questions, because otherwise
 *  the values the user has entered will be lost upon redrawing.
 * @param section_id
 */
function save_section(section_id) {
    $.when(store_section(section_id)).then(function (section_api_resp) {
        var section_data = section_api_resp.data;
        var new_section_id = section_data.id;
        $('#questions_section_' + section_id).find('.question').each(function(){
            var id_parts = $(this).attr('id').split('_');
            var question_id = id_parts[id_parts.length - 1];
            $.when(store_question(question_id, new_section_id)).then(function (question_api_resp) {
                var question_data = question_api_resp.data;
                redraw_question(question_id, question_data, section_id);
            });
        });
        redraw_section(section_id, section_data);
    });
}

/**
 * Store a section.
 * Returns $.ajax().
 * @param section_id
 * @returns {*}
 */
function store_section(section_id) {
    var report_id = $('#report_id').attr('value');
    var data = {
        report_id: report_id
    };
    for (var i = 0; i < section_data_fields.length; i++) {
        data[section_data_fields[i]] = $('#section_' + section_data_fields[i] + '_' + section_id).val();
    }
    /* If section_id < 0, we have to create a new section */
    var method = 'PUT';
    var url = '/api/v2/section/' + section_id;
    if (section_id < 0) {
        method = 'POST';
        url = '/api/v2/section';
    }
    return $.ajax({
        method: method,
        url: url,
        data: JSON.stringify(data),
        /*async: false, /* We don't want this to return immediately, as we call it in save_question to get the id
         of the new section. If this returns immediately, we get the old ID. */
        success: function (data, status) {

        },
        error: function (jqXHR, status, error) {
            $('#section_' + section_id + '_save_button').html(error_button(error));
            /* Add change handlers */
            for (i = 0; i < section_data_fields.length; i++) {
                add_change_handler(section_id, '#section_' + section_data_fields[i] + '_' + section_id);
            }
        }
    });
}

/**
 * Redraw an existing section, keeping the questions.
 * @param old_section_id (the original section_id, e.g. -1 if it is a new one)
 * @param section_data
 */
function redraw_section(old_section_id, section_data) {
    /* Redraw the template, but keep the questions */
    /* We could just get the questions from the API again, but
     this might cause the work a user just has done in an
     unsaved question to be lost.
     We cannot simply first save the questions, as you can't
     create a new question without an existing section_id.
     So you wouldn't be able to create a new section with a
     new question and save it.
     Better options might be available. */
    var questions = $('#questions_section_' + old_section_id).contents().clone(true);
    /* We use the old, negative, section_id */
    /* As you can only save a section when aria-expanded is true, we keep this setting
     to prevent panels from closing abruptly, confusing users. */
    var aria_state = $('#section_panel_' + old_section_id).find('.panel-heading').attr('aria-expanded');
    var new_section_id = section_data.id;
    var section_template = $.templates('#section-template');
    var new_section_data = {
        section_id: new_section_id
    };
    for (var i = 0; i < section_data_fields.length; i++) {
        new_section_data['section_' + section_data_fields[i]] = section_data[section_data_fields[i]];
    }

    $('#section_panel_' + old_section_id).replaceWith(section_template.render(new_section_data));
    $('#questions_section_' + new_section_id).replaceWith(questions);
    $('#section_' + new_section_id + '_remove_button').find('button')
        .click(function () {
            delete_section(new_section_id);
        });
    $('#section_' + new_section_id + '_save_button').html(success_button('Saved'));
    /* Add change handlers */
    for (i = 0; i < section_data_fields.length; i++) {
        add_change_handler(new_section_id, '#section_' + section_data_fields[i] + '_' + new_section_id);
    }
    /* Collapsed or not? */
    if (aria_state == 'true') {
        set_collapsed_state('#section_panel_' + new_section_id);
    }
}

/**
 * Delete a section.
 * If section_id < 0, just remove it from the DOM.
 * Else, also remove it via the API.
 * @param section_id
 */
function delete_section(section_id) {
    /* Call DELETE on all dependent questions */
    $('#questions_section_' + section_id).find('.question').each(function () {
        var id_parts = $(this).attr('id');
        if (typeof(id_parts) !== 'undefined') {
            id_parts = id_parts.split('_');
            delete_question(id_parts[id_parts.length - 1]);
        }
    });
    if (section_id < 0) {
        $('#section_panel_' + section_id).remove();
    } else {
        return $.ajax({
            method: 'DELETE',
            url: '/api/v2/section/' + section_id,
            success: function (data, status) {
                $('#section_panel_' + section_id).remove();
            },
            error: function (jqXHR, status, error) {
                $('#section_' + section_id + '_remove_button').html(error_button(error));
            }
        });
    }
}

/**
 * Add .change handlers to reset the buttons to their default state when the
 * user changes something in an input field.
 * @param section_id
 * @param field_selector
 */
function add_change_handler(section_id, field_selector) {
    $(field_selector).change(function () {
        $('#section_' + section_id + '_save_button')
            .html(save_button('Save'))
            .find('button').click(function () {
            save_section(section_id);
        });
        $('#section_' + section_id + '_remove_button')
            .html(default_button('Remove'))
            .find('button').click(function () {
            delete_section(section_id);
        });
    });
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
