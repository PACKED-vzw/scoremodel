/**
 * Created by pieter on 17/05/16.
 */



$(document).ready(function(){
    /*
    Update the score to its initial value
     */
    update_score();
    /*
    Add the onchange event to fire when a new answer is selected
     */
    $('input[type=radio]').change(function(){
        var user_report_id = $('#report_id').attr('value');
        var question_id = get_question_id(this.name);
        submit_answer(user_report_id, question_id, this.value);
        update_score();
    });
});


/**
 * Get the question_id from the 'name' attribute on the 'input type=radio' element
 * for answers.
 * The name attribute is of the form 'questions_{question_id}' (e.g. questions_1)
 * @param name_attr
 * @return string
 */
function get_question_id(name_attr){
    var name_attr_split = name_attr.split('_');
    return name_attr_split[1];
}

/**
 * Update the score using API calls:
 *  - Get all questions for this section.
 *  - For all questions, get the QuestionAnswer
 *      - If one exists: score = score + question_score * question_multiply
 *      - If one doesn't: score = score + 0
 *      - Set the score
 */
function update_score() {
    /*
    First, get all questions for the current section (input section_id)
     */
    var section_id = $('#section_id').attr('value');
    var user_report_id = $('#report_id').attr('value');
    $.ajax({
        method: 'GET',
        url: '/api/v2/section/' + section_id,
        success: function(data, status) {
            var questions = data.data.questions;
            /*
             Second, get the question_answer for every question (if they exist)
             */
            var score = 0;
            for (var i = 0; i < questions.length; i++) {
                /*
                While it would be easier to update the score synchronously, this is not necessary.
                 */
                $.ajax({
                    method: 'GET',
                    url: '/api/v2/user_report/' + user_report_id + '/question/' + questions[i].id,
                    success: function(data, status) {
                        /*
                         Third add up all the (score * multiplication_factor)
                         */
                        score = score + (data.data.score * data.data.multiplication_factor);
                        set_score(score);
                    },
                    error: function(jqXHR, status, error) {
                        if (error == 'NOT FOUND') {
                            /*
                            If the QA was not found, this question has not been answered, so increment the
                            score with 0
                             */
                            score = score + 0;
                            set_score(score);
                        } else {
                            console.log(error);
                        }
                    }
                });
            }
        },
        error: function(jqXHR, status, error){
            console.log(error);
        }
    });
}

function set_score(score) {
    /*
             Fourth, round to int
             */
            /*
             Fifth, set <span id="score">
             */
    var rounded_score = Math.round(score);
    $('#score').html(rounded_score);
}

/**
 * Submit a new (or modified) answer to the upstream API.
 * @param user_report_id
 * @param question_id
 * @param answer_id
 */
function submit_answer(user_report_id, question_id, answer_id){
    $.ajax({
        method: 'GET',
        url: '/api/v2/user_report/' + user_report_id + '/question/' + question_id,
        success: function(data, status){
            /*
            When successful, this combination already exists. If so, get the ID from data.data and perform a PUT
            request.
             */
            var question_answer_id = data.data.id;
            $.ajax({
                method: 'PUT',
                url: '/api/v2/question_answer/' + question_answer_id,
                data: JSON.stringify({
                    user_report_id: user_report_id,
                    question_id: question_id,
                    answer_id: answer_id
                }),
                success: function(data, status){
                    //console.log(status);
                },
                error: function(jqXHR, status, error){
                    console.log(error);
                }
            });
        },
        error: function(jqXHR, status, error){
            /*
            If it doesn't exist, use a POST request to /api/v2/question_answer
             */
            console.log(status);
            if (error == 'NOT FOUND') {
                $.ajax({
                    method: 'POST',
                    url: '/api/v2/question_answer',
                    data: JSON.stringify({
                        user_report_id: user_report_id,
                        question_id: question_id,
                        answer_id: answer_id
                    }),
                    success: function(data, status){},
                    error: function(jqXHR, status, error){}
                });
            } else {
                console.log(error);
            }
        }
    });
}





