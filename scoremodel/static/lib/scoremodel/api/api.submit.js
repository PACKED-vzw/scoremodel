/**
 * Created by pieter on 7/01/16.
 */

var api_submit = angular.module('scoremodel.api_submit', ['scoremodel.api_core']);

api_submit.factory('ApiSubmit', ['ApiCore',
    function(ApiCore) {
        var ApiSubmit = function(report) {
            /**
             * This class submits any updates to the API. It uses the internal .id property to check
             * whether it has to POST or PUT (create or update). It returns the promise for the API reply.
             */
            this.a_api = new ApiCore();
            this.scope_report = report;
        };

        /**
         * Submit a report. Checks this.scope_report.id whether it is less than 0 (create) or not (update).
         * @returns {*}
         */
        ApiSubmit.prototype.report = function() {
            var a_report = new ConvertReport();
            var cleaned_data = a_report.to_api(this.scope_report);
            var api_promise;
            if (this.scope_report.id < 0) {
                /* Create */
                api_promise = this.a_api.create(cleaned_data, 'report');
            } else {
                /* Update */
                api_promise = this.a_api.update(this.scope_report.id, cleaned_data, 'report');
            }
            return api_promise;
        };

        /**
         * Submit a section. Requires section_id to know which section of this.scope_report needs to be submitted.
         * @param section_id
         * @returns {*}
         */
        ApiSubmit.prototype.section = function(section_id) {
            var a_section = new ConvertSection();
            /* Clean data */
            var cleaned_data = null;
            for (var i = 0; i < this.scope_report.sections.length; i++) {
                var section = this.scope_report.sections[i];
                if (section_id == section.id) {
                    cleaned_data = a_section.to_api(section, this.scope_report.id);
                    break;
                }
            }
            if (cleaned_data === null) {
                console.log('Failed to find section');
            }
            /* API */
            var api_promise;
            if (section_id < 0) {
                /* Create */
                api_promise = this.a_api.create(cleaned_data, 'section');
            } else {
                /* Update */
                api_promise = this.a_api.update(section_id, cleaned_data, 'section');
            }
            return api_promise;
        };

        /**
         * Submit a question. Requires section_id and question_id to know which question needs to be submitted.
         * @param section_id
         * @param question_id
         */
        ApiSubmit.prototype.question = function(section_id, question_id) {
            var a_question = new ConvertQuestion();
            /* Clean data */
            var cleaned_data = null;
            for (var i = 0; i < this.scope_report.sections.length; i++) {
                var section = this.scope_report.sections[i];
                if (section_id == section.id) {
                    for (var j = 0; j < section.questions.length; j++) {
                        var question = section.questions[j];
                        if (question_id == question.id) {
                            cleaned_data = a_question.to_api(question, section.id);
                            break;
                        }
                    }
                    break;
                }
            }
            if (cleaned_data == null) {
                console.log('Failed to find question');
            }
            /* API */
            var api_promise;
            if (question_id < 0) {
                /* Create */
                api_promise = this.a_api.create(cleaned_data, 'question');
            } else {
                /* Update */
                api_promise = this.a_api.update(question_id, cleaned_data, 'question');
            }
            return api_promise;
        };

        /**
         * 
         */
        ApiSubmit.prototype.question_answer = function(report_id, question_id, answer_id, question_answer_id) {
            var input_data = {
                user_report_id: report_id,
                question_id: question_id,
                answer_id: answer_id
            };
            var api_promise;
            if (question_answer_id < 0) {
                /* Create */
                api_promise = this.a_api.create(input_data, 'user_report/question_answer');
            } else {
                /* Update */
                api_promise = this.a_api.update(question_answer_id, input_data, 'user_report/question_answer');
            }
            return api_promise;
        };

        return ApiSubmit;
    }
]);

