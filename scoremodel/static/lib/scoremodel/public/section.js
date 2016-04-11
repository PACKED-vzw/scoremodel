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
        
        $scope.submit_answer = function(report_id, question_id, answer_id) {
            /*
            if not questions[id].question_answer_id: set to -1
             */
            var api_submit = new ApiSubmit(null);
            var submit_promise;
            if () {
                $scope.questions[question_id] = {
                    question_answer_id: -1,
                    error: {}
                };
                submit_promise = api_submit.question_answer(report_id, question_id, answer_id, -1);
            } else {
                submit_promise = api_submit.question_answer(report_id, question_id, answer_id, $scope.questions[question_id].question_answer_id);
            }
            submit_promise.then(function success(response){
                $scope.questions[question_id].question_answer_id = response.data.data.id;
            }, function error(response){
                $scope.questions[question_id].error.msg = response;
            });
        };
    }
]);
