/**
 * Created by pieter on 7/07/16.
 */

function add_question_button(section_id) {
    var last_question_id_el = $('#last_question_id');
    var last_question_id = parseInt(last_question_id_el.val()) - 1;
    last_question_id_el.val(last_question_id);
    var question_data = {
        id: last_question_id,
        section_id: section_id,
        answers: []
    };
    $('#questions_section_' + section_id).append(draw_question_template(question_data));
    add_section_focus_handlers(last_question_id);
    add_section_click_handlers(last_question_id);
}

function delete_question_button(question_id) {
}

function save_question_button(question_id) {
}

function save_question_data(question_id) {
}

function delete_question_data(question_id) {
}

function get_question_data(question_id) {
    return $.ajax({
        url: '/api/v2/question/' + question_id,
        method: 'GET',
        success: function (data, status) {
        },
        error: function (jqXHR, status, error) {
            error_button('#question_' + question_id + '_save_button', error);
        }
    });
}

function draw_question(deferred, is_first_time, old_question_id) {
    if (deferred) {
        $.when(deferred).then(function success(question_api_data) {
            var question = question_api_data.data;
            if (old_question_id) {
                replace_existing_question(old_question_id, question);
            } else {
                $('#questions_section_' + question.section_id).append(draw_question_template(question));
                /* Selected answer */
                for (var i = 0; i < question.answers.length; i++) {
                    var answer_id = question.answers[i].id;
                    $('#question_answer_' + question.id)
                        .find('select option[value=' + answer_id + ']').attr("selected", "selected");
                }
                /* Selected risk factor */
                $('#question_risk_factor_' + question.id)
                    .find('select option[value=' + question.risk_factor_id + ']').attr("selected", "selected");
            }
            if (is_first_time) {
                add_question_focus_handlers(question.id);
                add_question_click_handlers(question.id);
            }
        });
    }
}

function draw_question_template(question_data) {
    var question_template = $.templates('#question-template');
    var template_data = {
        question_id: question_data.id,
        section_id: question_data.section_id,
        question_question: question_data.question,
        question_weight: question_data.weight,
        question_example: question_data.example,
        question_context: question_data.context,
        question_risk: question_data.risk,
        question_action: question_data.action
    };
    return question_template.render(template_data);
}

function replace_existing_question(old_question_id, question_data) {
    var old_question = $('#question_' + old_question_id);
    /* As you can only save a section when aria-expanded is true, we keep this setting
     to prevent panels from closing abruptly, confusing users. */
    var aria_state = old_question.find('.panel-heading').attr('aria-expanded');
    var new_question_id = question_data.id;
    old_question.replaceWith(draw_question_template(question_data));
    /* Collapsed or not? */
    if (aria_state == 'true') {
        set_collapsed_state('#question_panel_' + new_question_id);
    }
    /* Answers and risk_factor */
    /* Selected answer */
    for (var i = 0; i < question_data.answers.length; i++) {
        var answer_id = question_data.answers[i].id;
        $('#question_answer_' + new_question_id)
            .find('select option[value=' + answer_id + ']').attr("selected", "selected");
    }
    /* Selected risk factor */
    $('#question_risk_factor_' + new_question_id)
        .find('select option[value=' + question_data.risk_factor_id + ']').attr("selected", "selected");

    add_question_focus_handlers(new_question_id);
    add_question_click_handlers(new_question_id);

    success_button('#question_' + new_question_id + '_save_button', 'Saved');
}

function add_question_focus_handlers(question_id) {
    var fields = ['question_weight_' + question_id, 'question_question_' + question_id,
        'question_example_' + question_id, 'question_context_' + question_id,
        'question_risk_' + question_id, 'question_action_' + question_id,
        'question_answer_' + question_id, 'question_risk_factor_' + question_id];
    for (var i = 0; i < fields.length; i++) {
        $('#' + fields[i]).focus(function () {
            default_button('#question_' + question_id + '_save_button', 'Save');
            default_button('#question_' + question_id + '_remove_button', 'Remove');
        });
    }
}

function add_question_click_handlers(question_id) {
    $('#section_' + question_id + '_save_button').click(function () {
        // weight question risk_factor answer
        if (required_set_side_effects(['#question_weight_' + question_id, '#question_question_' + question_id,
                '#question_answer_' + question_id, '#question_risk_factor_' + question_id])) {
            save_question_button(question_id);
        }
    });
    $('#question_' + question_id + '_remove_button').click(function () {
        delete_question_button(question_id);
    });
}