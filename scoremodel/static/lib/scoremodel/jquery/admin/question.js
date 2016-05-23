/**
 * Created by pieter on 23/05/16.
 */

$(document).ready(function(){
    
});

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
}
