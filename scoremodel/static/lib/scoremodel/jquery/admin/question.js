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
    add_question_focus_handlers(last_question_id);
    add_question_click_handlers(last_question_id);
}

function delete_question_button(question_id) {
    if (question_id < 0) {
        $('#question_' + question_id).remove();
    } else {
        $.when(delete_question_data(question_id)).then(function () {
            $('#question_' + question_id).remove();
        });
    }
}

function question_data_from_form(question_id) {
    var question_data = {
        section_id: $('#question_section_id_' + question_id).val(),
        question: $('#question_question_' + question_id).val(),
        weight: $('#question_weight_' + question_id).val(),
        example: $('#question_example_' + question_id).val(),
        context: $('#question_context_' + question_id).val(),
        risk: $('#question_risk_' + question_id).val(),
        action: $('#question_action_' + question_id).val(),
        risk_factor_id: $('#question_risk_factor_' + question_id).val(),
        answers: [],
        id: question_id
    };
    var answers = $('#question_answer_' + question_id).val();
    if (answers !== null) {
        /* The API expects this to be an array */
        question_data.answers = answers;
    }
    return question_data;
}

function delete_question_data(question_id) {
    return $.ajax({
        method: 'DELETE',
        url: '/api/v2/question/' + question_id,
        success: function (data, status) {
        },
        error: function (jqXHR, status, error) {
            error_button('#report_save_button', error);
        }
    });

}

function get_question_data(question_id) {
    return $.ajax({
        url: '/api/v2/question/' + question_id,
        method: 'GET',
        success: function (data, status) {
        },
        error: function (jqXHR, status, error) {
            error_button('#report_save_button', error);
        }
    });
}

function draw_question(deferred, is_first_time) {
    if (deferred) {
        $.when(deferred).then(function success(question_api_data) {
            var question = question_api_data.data;
            var questions =  $('#questions_section_' + question.section_id);
            questions
                .find('#question_id_placeholder_' + question.id)
                .replaceWith(draw_question_template(question));
            /* Selected answer */
            for (var i = 0; i < question.answers.length; i++) {
                var answer_id = question.answers[i].id;
                $('#question_answer_' + question.id)
                    .find('option[value=' + answer_id + ']').attr("selected", "selected");
            }
            /* Selected risk factor */
            $('#question_risk_factor_' + question.id)
                .find('option[value=' + question.risk_factor_id + ']').attr("selected", "selected");
            
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

function add_question_focus_handlers(question_id) {
    var fields = ['question_weight_' + question_id, 'question_question_' + question_id,
        'question_example_' + question_id, 'question_context_' + question_id,
        'question_risk_' + question_id, 'question_action_' + question_id,
        'question_answer_' + question_id, 'question_risk_factor_' + question_id];
    for (var i = 0; i < fields.length; i++) {
        $('#' + fields[i]).focus(function () {
            default_button('#report_save_button', 'Save');
        });
    }
}

function add_question_click_handlers(question_id) {
    $('#question_' + question_id + '_remove_button').click(function () {
        delete_question_button(question_id);
    });
}


function required_check_question(question_id) {
    var required = ['#question_weight_' + question_id, '#question_question_' + question_id,
        '#question_risk_factor_' + question_id, '#question_answer_' + question_id];
    return required_set_side_effects(required);
}
