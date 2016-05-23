/**
 * Created by pieter on 23/05/16.
 */

$(document).ready(function(){
    
});

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
        question_id: question.id,
        question_title: question.question,
        question_weight: question.weight,
        question_example: question.example,
        question_context: question.context,
        question_risk: question.risk,
        question_action: question.action
    };
    $('#questions_section_' + section_id).append(question_template.render(template_vars));
    /* Set selected answer(s) */
    for(var i = 0; i < question.answers.length; i++) {
        var answer_id = question.answers[i].id;
        $('#question_answer_' + question.id)
            .find('select option[value=' + answer_id + ']').attr("selected", "selected");
    }
    /* Set selected risk_factor */
    $('#question_risk_factor_' + question.id)
        .find('select option[value=' + question.risk_factor_id + ']').attr("selected", "selected");

    /* Add .click-callback to the save button */
    $('#question_' + question.id + '_save_button').find('button')
        .click(function(){
            save_question(question.id, section_id);
        });
    $('#question_' + question.id + '_remove_button').find('button')
        .click(function(){
            delete_question(question.id, section_id);
        });
    return true;
}

/**
 * Save the current question
 * @param question_id
 * @param section_id
 */
function save_question(question_id, section_id) {
    var data = {
        section_id: section_id,
        question:  $('#question_question_' + question_id).val(),
        weight: $('#question_weight_' + question_id).val(),
        example: $('#question_example_' + question_id).val(),
        context: $('#question_context_' + question_id).val(),
        risk: $('#question_risk_' + question_id).val(),
        action: $('#question_action_' + question_id).val(),
        risk_factor_id: $('#question_risk_factor_' + question_id).find('select').val(),
        answers: $('#question_answer_' + question_id).find('select').val()
    };
    console.log(data);
}

function delete_question(question_id, section_id) {}
