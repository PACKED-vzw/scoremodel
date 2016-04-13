/**
 * Created by pieter on 11/04/16.
 */

var app = angular.module('scoremodel.public', ['scoremodel.api_core', 'scoremodel.api_submit']);

app.controller('SectionCtrl', ['$scope', 'ApiCore', 'ApiSubmit',
    function($scope, ApiCore, ApiSubmit) {
        /**
         * Submit the answer to a question to the API.
         * @param report_id
         * @param question_id
         * @param answer_id
         */
        $scope.questions = {};
        $scope.answers = {};



        $scope.fill_model = function() {
            var parse_url = new UrlParse('');
            var section_id = parse_url.get_str_id('section_id');
            var user_report_id = parse_url.get_str_id('report_id');
            var api_core = new ApiCore();
            var promise = api_core.read(section_id, 'section');
            promise.then(function success(response){
                for(var i = 0; i < response.data.data.questions.length; i++) {
                    var question = response.data.data.questions[i];
                    $scope.answers[question.id] = {answer: null};
                    var question_answer_promise = api_core.read(user_report_id + '/question/' + question.id, 'user_report');
                    question_answer_promise.then(function success(response) {
                        var question_answer = response.data.data;
                        $scope.answers[question_answer.question_id].answer = question_answer.answer_id;
                        $scope.answers[question_answer.question_id].question_answer_id = question_answer.id;
                    }, function error(response){});
                }
            }, function error(response){});
        };
        
        $scope.submit_answer = function(report_id, question_id, answer_id) {
            /*
            if not questions[id].question_answer_id: set to -1
             */
            var api_submit = new ApiSubmit(null);
            var submit_promise;
            if (!$scope.answers[question_id].hasOwnProperty('question_answer_id')) {
                $scope.answers[question_id].question_answer_id = -1;
                submit_promise = api_submit.question_answer(report_id, question_id, answer_id, -1);
            } else {
                submit_promise = api_submit.question_answer(report_id, question_id, answer_id, $scope.answers[question_id].question_answer_id);
            }
            submit_promise.then(function success(response){
                $scope.answers[question_id].question_answer_id = response.data.data.id;
            }, function error(response){
                $scope.answers[question_id].error = response;
            });
        };

        $scope.fill_model();
    }
]);
