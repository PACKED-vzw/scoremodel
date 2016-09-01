$(document).ready(function(){
    /*
    Add the onchange event to fire when a new answer is selected
     */
    $('input[type=radio]').change(function(){
        var benchmark_report_id = $('#report_id').attr('value');
        var question_id = get_question_id(this.name);
        submit_benchmark(benchmark_report_id, question_id, this.value);
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
 * Submit a new (or modified) benchmark to the upstream API.
 * @param benchmark_report_id
 * @param question_id
 * @param answer_id
 */
function submit_benchmark(benchmark_report_id, question_id, answer_id){
    $.ajax({
        method: 'GET',
        url: '/api/v2/benchmark_report/' + benchmark_report_id + '/question/' + question_id,
        success: function(data, status){
            /*
            When successful, this combination already exists. If so, get the ID from data.data and perform a PUT
            request.
             */
            var benchmark_id = data.data.id;
            var benchmark_data = {
                benchmark_report_id: benchmark_report_id,
                question_id: question_id
            };
            if (answer_id > 0) {
                benchmark_data['answer_id'] = answer_id;
            }


            $.ajax({
                method: 'PUT',
                url: '/api/v2/benchmark/' + benchmark_id,
                headers: {
                        'X-CSRFToken': csrf_token
                    },
                contentType: 'application/json',
                data: JSON.stringify(benchmark_data),
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
                var benchmark_data = {
                    benchmark_report_id: benchmark_report_id,
                    question_id: question_id
                };
                if (answer_id > 0) {
                    benchmark_data['answer_id'] = answer_id;
                }

                $.ajax({
                    method: 'POST',
                    url: '/api/v2/benchmark',
                    contentType: 'application/json',
                    headers: {
                        'X-CSRFToken': csrf_token
                    },
                    data: JSON.stringify(benchmark_data),
                    success: function(data, status){},
                    error: function(jqXHR, status, error){}
                });
            } else {
                console.log(error);
            }
        }
    });
}





