/**
 * Created by pieter on 23/05/16.
 */

// TODO: required fields

var question_keys = ['question', 'weight', 'example', 'context', 'risk', 'action'];

$(document).ready(function () {

});

/**
 * Add a new (empty) question.
 * @param section_id
 * @returns {boolean}
 */
function new_question(section_id) {
    var last_id_el = $('#last_question_id');
    var last_id = last_id_el.attr('value');
    var question = {
        id: last_id - 1,
        answers: []
    };
    last_id_el.attr('value', last_id - 1);
    return add_question(question, section_id);
}

/**
 * From a question object (API), add a new question to the DOM.
 *  - Get the template (jsrender) called '#question-template'
 *  - Fill in all variables.
 *  - Render it.
 *  - Append it to #questions_sections_ + section_id
 * @param question
 * @param section_id
 * @returns {boolean}
 */
function add_question(question, section_id) {
    var question_template = $.templates('#question-template');
    var template_vars = {
        question_id: question.id
    };
    for (var i = 0; i < question_keys.length; i++) {
        template_vars['question_' + question_keys[i]] = question[question_keys[i]];
    }

    $('#questions_section_' + section_id).append(question_template.render(template_vars));
    /* Set selected answer(s) */
    for (i = 0; i < question.answers.length; i++) {
        var answer_id = question.answers[i].id;
        $('#question_answer_' + question.id)
            .find('select option[value=' + answer_id + ']').attr("selected", "selected");
    }
    /* Set selected risk_factor */
    $('#question_risk_factor_' + question.id)
        .find('select option[value=' + question.risk_factor_id + ']').attr("selected", "selected");

    /* Add .click-callback to the save button */
    $('#question_' + question.id + '_save_button')
        .click(function () {
            console.log('clicked');
            save_question(question.id, section_id);
        });
    $('#question_' + question.id + '_remove_button')
        .click(function () {
            delete_question(question.id, section_id);
        });
    for (i = 0; i < question_keys.length; i++) {
        add_change_handler(question.id, section_id, '#question_' + question_keys[i] + '_' + question.id);
    }
    return true;
}

/**
 * Save the current question
 * @param question_id
 * @param section_id
 */
function save_question(question_id, section_id) {
    /* If the section_id < 0, this is a new question in a new (unsaved)
     section. We can't store that, so we first have to save the
     section. */
    if (section_id < 0) {
        save_section(section_id);
    } else {
        $.when(store_question(question_id, section_id)).then(
            function success(question_api_response) {
                console.log(question_api_response.data);
                success_button('#question_' + question_api_response.data.id + '_save_button', 'Saved');
            },
            function error(jqXHR, status, error) {
                error_button('#question_' + question_id + '_save_button', error);
            }
        );
    }

}

/**
 * Store a question. This has been lifted from save_question
 * so it can support async $.ajax calls when saving sections
 * that need to exist before a question can be submitted.
 * @param question_id
 * @param section_id
 */
function store_question(question_id, section_id) {
    var data = {
        section_id: section_id,
        risk_factor_id: $('#question_risk_factor_' + question_id).find('select').val(),
        answers: []
    };
    var answers = $('#question_answer_' + question_id).find('select').val();
    if (answers !== null) {
        data.answers = answers;
    }
    for (var i = 0; i < question_keys.length; i++) {
        data[question_keys[i]] = $('#question_' + question_keys[i] + '_' + question_id).val();
    }

    /* If question_id < 0, then it is a new question */
    var method = 'PUT';
    var url = '/api/v2/question/' + question_id;
    if (question_id < 0) {
        method = 'POST';
        url = '/api/v2/question';
    }

    return $.ajax({
        url: url,
        method: method,
        data: JSON.stringify(data),
        success: function (data, status) {
        },
        error: function (jqXHR, status, error) {
            error_button('#question_' + question_id + '_save_button', error);
            /* Add change handlers */
            for (i = 0; i < question_keys.length; i++) {
                add_change_handler(question_id, section_id, '#question_' + question_keys[i] + '_' + question_id);
            }
        }
    });
}

/**
 * Redraw the a question (question_data) using the template.
 * @param old_question_id
 * @param question_data
 * @param section_id
 */
function redraw_question(old_question_id, question_data, section_id) {
    /* Redraw the template */
    var old_question = $('#question_' + old_question_id);
    var aria_state = old_question.find('.panel-heading').attr('aria-expanded');
    var new_question_id = question_data.id;
    var question_template = $.templates('#question-template');
    var new_question_data = {
        question_id: new_question_id
    };
    for (var i = 0; i < question_keys.length; i++) {
        new_question_data['question_' + question_keys[i]] = question_data[question_keys[i]];
    }
    old_question.replaceWith(question_template.render(new_question_data));
    /* Saved button */
    success_button('#question_' + new_question_id + '_save_button', 'Saved');
    /* Set selected answer(s) */
    for (i = 0; i < question_data.answers.length; i++) {
        var answer_id = question_data.answers[i].id;
        $('#question_answer_' + new_question_id)
            .find('select option[value=' + answer_id + ']').attr("selected", "selected");
    }
    /* Set selected risk_factor */
    $('#question_risk_factor_' + new_question_id)
        .find('select option[value=' + question_data.risk_factor_id + ']').attr("selected", "selected");

    /* Add change handlers */
    for (i = 0; i < question_keys.length; i++) {
        add_change_handler(new_question_id, section_id, '#question_' + question_keys[i] + '_' + new_question_id);
    }
    /* Collapsed or not? */
    if (aria_state == 'true') {
        set_collapsed_state('#question_' + new_question_id);
    }
    /* Delete button */
    $('#question_' + new_question_id + '_remove_button')
        .click(function () {
            delete_question(new_question_id, section_id);
        });
}

/**
 * Delete a question.
 * @param question_id
 */
function delete_question(question_id) {
    if (question_id < 0) {
        $('#question_' + question_id).remove();
    } else {
        $.ajax({
            method: 'DELETE',
            url: '/api/v2/question/' + question_id,
            success: function (data, status) {
                $('#question_' + question_id).remove();
            },
            error: function (jqXHR, status, error) {
                error_button('#question_' + question_id + '_remove_button', error);
            }
        });
    }
}

/**
 * Get the ID of the parent section of the current question.
 * @param question_id
 * @returns {*}
 */
function get_parent_section_id(question_id) {
    var parent_section = $('#question_' + question_id).parent();
    var section_id_parts = parent_section.attr('id').split('_');
    return section_id_parts[section_id_parts.length - 1];
}

/* TODO: Change handlers bug */
/**
 * Add .change handlers to reset the buttons to their default state when the
 * user changes something in an input field.
 * @param question_id
 * @param section_id
 * @param field_selector
 */
function add_change_handler(question_id, section_id, field_selector) {
    $(field_selector).focus(function () {
        $('#question_' + question_id + '_save_button')
            .click(function () {
                save_question(question_id, section_id);
            });
        default_button('#question_' + question_id + '_save_button', 'Save');
        $('#question_' + question_id + '_remove_button')
            .click(function () {
                delete_question(question_id, section_id);
            });
        default_button('#question_' + question_id + '_remove_button', 'Remove');
    });
}
