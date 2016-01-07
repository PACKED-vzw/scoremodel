/**
 * Created by pieter on 4/01/16.
 */

var app = angular.module('scoremodel', ['scoremodel.api_core', 'scoremodel.api_submit']);

app.controller('AdminCtrl', ['$scope', '$location', '$q', 'ApiCore', 'ApiSubmit',
    function($scope, $location, $q, ApiCore, ApiSubmit) {
        /**
         * Reset all errors or one ($scope.errors.action) to their default values
         * @param action optional action parameter (attribute of $scope.errors)
         * @param item_id
         */
        $scope.reset_errors = function(action, item_id) {
            if (action == null) {
                $scope.errors = {
                    report_submit: {},
                    report_remove: {},
                    report_new: {},
                    section_submit: {},
                    section_remove: {},
                    section_new: {},
                    question_submit: {},
                    question_remove: {},
                    question_new: {}
                };
            } else {
                $scope.errors[action][item_id] = false;
            }
        };

        /**
         * Reset all success or one ($scope.success.action) to their default values
         * @param action optional action parameter (attribute of $scope.success)
         * @param item_id
         */
        $scope.reset_success = function(action, item_id) {
            if (action == null) {
                $scope.success = {
                    report_submit: {},
                    report_remove: {},
                    report_new: {},
                    section_submit: {},
                    section_remove: {},
                    section_new: {},
                    question_submit: {},
                    question_remove: {},
                    question_new: {}
                };
            } else {
                $scope.success[action][item_id] = false;
            }
        };

        /**
         * Reset the submit button for a form (via ng-change)
         * @param action
         * @param item_id
         */
        $scope.reset_submit_button = function(action, item_id) {
            $scope.reset_success(action, item_id);
            $scope.reset_errors(action, item_id);
        };

        /*
        Reset all errors & success
         */
        $scope.reset_errors();
        $scope.reset_success();

        /*
        Keep track of the IDs we gave to new_sections and new_questions, so no duplicates exist.
        IDs of items not yet committed to the API are < 0; the API only sends IDs > 0
         */
        $scope.new_section_id = -1;
        $scope.new_question_id = -1;

        /*
        Template for empty reports, sections etc.
         */
        $scope.report_template = {
            title: 'Nieuw rapport',
            sections: [
                {
                    id: -1,
                    title: 'Nieuwe sectie',
                    order_in_report: 0,
                    context: '',
                    total_score: 0,
                    questions: [
                        {
                            id: -1,
                            title: 'Nieuwe vraag',
                            weight: 1,
                            order_in_section: 0,
                            context: '',
                            answers: $scope.available_answers,
                            example: '',
                            section_id: 0,
                            risk: '',
                            question: 'Nieuwe vraag',
                            action: '',
                            risk_factors: $scope.available_risk_factors
                        }
                    ]
                }
            ]
        };

        /**
         * Submit functions
         * TODO replace switch-case with something more robust (?)
         */
        /**
         * Submit the form. var primary contains the primary part of the form that has been changed and
         * that the user wants to save (report, section or question). However, to prevent information loss
         * the script checks all other parts to see if any have been changed ($touched). If so, it saves them
         * as well.
         * @param primary
         * @param section_id
         * @param question_id
         */
        $scope.submit_form = function(primary, section_id, question_id) {
            /*
            $scope.report contains all
             */
            var a_submit = new ApiSubmit($scope.report);
            var submit_promise;
            switch(primary) {
                case 'report':
                    submit_promise = a_submit.report();
                    break;
                case 'section':
                    if (section_id == null) {
                        alert('No section_id');
                        console.log('No section_id. Not saved.')
                    } else {
                        submit_promise = a_submit.section(section_id);
                    }
                    break;
                case 'question':
                    if (section_id == null || question_id == null) {
                        alert('No section_id or question_id');
                        console.log('No section_id or question_id. Not saved.')
                    } else {
                        submit_promise = a_submit.question(section_id, question_id);
                    }
                    break;
            }
            /*
            Submit to the server
             */
            submit_promise.then(function success(response){
                /*
                Update only what was changed
                The 'response' returned by the API returns the new/updated object; so for question it only returns the
                new question. We only replace that one, so the user doesn't lose anything (unless he did not save his stuff)
                 */
                switch(primary) {
                    case 'report':
                        $scope.success['report_submit'][$scope.report.id] = true;
                        var a_report = new ConvertReport();
                        var new_report = a_report.from_api(response, $scope.available_answers, $scope.available_risk_factors);
                        new_report.sections = $scope.report.sections;
                        $scope.report = new_report;
                        break;
                    case 'section':
                        $scope.success['section_submit'][section_id] = true;
                        var a_section = new ConvertSection();
                        var new_section = a_section.from_api(response);
                        for (var i = 0; i < $scope.report.sections.length; i++) {
                            var section = $scope.report.sections[i];
                            if (section.id == section_id) {
                                new_section.questions = section.questions;
                                if (section_id < 0) {
                                    /* The ID we get from the API will never be below zero, so we're replacing a new one */
                                    $scope.report.sections[i] = new_section;
                                    /*
                                    The old section.id was -1, but this one is now removed, so set $scope.success[][new_id] = true
                                     */
                                    $scope.success['section_submit'][new_section.id] = true;
                                } else {
                                    /* Just a simple update */
                                    /* Note that for PUT, the ID of the section can never change, but checking regardless */
                                    if (section_id != new_section.id) {
                                        console.log('Original section id and new section id do not match');
                                    } else {
                                        $scope.report.sections[i] = new_section;
                                    }
                                }
                                break;
                            }
                        }
                        break;
                    case 'question':
                        $scope.success['question_submit'][question_id] = true;
                        var a_question = new ConvertQuestion();
                        var new_question = a_question.from_api(response, $scope.available_risk_factors);
                        for (i = 0; i < $scope.report.sections.length; i++) {
                            section = $scope.report.sections[i];
                            if (section.id == section_id) {
                                for (var j = 0; j < section.questions.length; j++) {
                                    var question = section.questions[j];
                                    if (question.id == question_id) {
                                        if (question_id < 0) {
                                            $scope.report.sections[i].questions[j] = new_question;
                                            $scope.success['question_submit'][new_question.id] = true;
                                        } else {
                                            if (question_id != new_question.id) {
                                                console.log('Original question id and new question id do not match');
                                            } else {
                                                $scope.report.sections[i].questions[j] = new_question;
                                            }
                                        }
                                        break;
                                    }
                                }
                                break;
                            }
                        }
                        break;
                }
            }, function error(response) {
                switch(primary) {
                    case 'report':
                        $scope.errors['report_submit'][$scope.report.id] = response.data.msg;
                        break;
                    case 'section':
                        $scope.errors['section_submit'][section_id] = response.data.msg;
                        break;
                    case 'question':
                        $scope.errors['question_submit'][question_id] = response.data.msg;
                        break;
                }
            });
        };

        /**
         * To add a new element
         * This new element always has the next available negative id ($scope.new_primary - 1).
         * @param primary
         * @param section_id
         */
        $scope.new_element_in_form = function(primary, section_id) {
            switch(primary) {
                case 'report':
                    /* Not implemented */
                    $scope.report = $scope.report_template;
                    break;
                case 'section':
                    $scope.new_section_id = $scope.new_section_id - 1;
                    var template_section = angular.copy($scope.report_template.sections[0]);
                    template_section.id = angular.copy($scope.new_section_id);
                    $scope.report.sections.push(template_section);
                    $scope.success.section_new[template_section.id] = true;
                    break;
                case 'question':
                    if (section_id != null) {
                        $scope.new_question_id = $scope.new_question_id - 1;
                        var template_question = angular.copy($scope.report_template.sections[0].questions[0]);
                        template_question.id = angular.copy($scope.new_question_id);
                        for (var i = 0; i < $scope.report.sections.length; i++) {
                            var section = $scope.report.sections[i];
                            if (section.id == section_id) {
                                $scope.report.sections[i].questions.push(template_question);
                                $scope.success.question_new[template_question.id] = true;
                                break;
                            }
                        }
                    } else {
                        console.log('No section id. Did nothing.');
                    }
                    break;
            }
        };

        /**
         * Remove an element. Elements can be committed to the API, in which case we
         * issue an apicore.delete() request, or not, in which case we remove it from their parent.
         * @param primary
         * @param section_id
         * @param question_id
         */
        $scope.remove_element = function(primary, section_id, question_id) {
            var a_api = new ApiCore();
            switch(primary) {
                case 'report':
                    /* Not implemented */
                    break;
                case 'section':
                    if (section_id != null) {
                        if (section_id < 0) {
                            /* Not yet committed to the API */
                            for (var i = 0; i < $scope.report.sections.length; i++) {
                                var section = $scope.report.sections[i];
                                if (section_id == section.id) {
                                    $scope.report.sections.splice(i, 1);
                                    $scope.success.section_remove[section_id] = true;
                                    break;
                                }
                            }
                        } else {
                            /* Already committed to the API */
                            a_api.delete(section_id, 'section').then(function success() {
                                for (var i = 0; i < $scope.report.sections.length; i++) {
                                    var section = $scope.report.sections[i];
                                    if (section_id == section.id) {
                                        $scope.report.sections.splice(i, 1);
                                        $scope.success.section_remove[section_id] = true;
                                        break;
                                    }
                                }
                            }, function error(response) {
                                $scope.errors.section_remove[section_id] = response.data.msg;
                            });
                        }
                    } else {
                        console.log('No section id. Did nothing.');
                    }
                    break;
                case 'question':
                    if (section_id != null && question_id != null) {
                        if (question_id < 0) {
                            /* Not in the API */
                            for (i = 0; i < $scope.report.sections.length; i++) {
                                if (section_id == $scope.report.sections[i].id) {
                                    for (var j = 0; j < $scope.report.sections[i].questions.length; j++) {
                                        if ($scope.report.sections[i].questions[j].id == question_id) {
                                            $scope.success.question_remove[question_id] = true;
                                            $scope.report.sections[i].questions.splice(j, 1);
                                            break;
                                        }
                                    }
                                    break;
                                }
                            }
                        } else {
                            /* In the API */
                            a_api.delete(question_id, 'question').then(function success() {
                                for (i = 0; i < $scope.report.sections.length; i++) {
                                    if (section_id == $scope.report.sections[i].id) {
                                        for (j = 0; j < $scope.report.sections[i].questions.length; j++) {
                                            if ($scope.report.sections[i].questions[j].id == question_id) {
                                                $scope.success.question_remove[question_id] = true;
                                                $scope.report.sections[i].questions.splice(j, 1);
                                                break;
                                            }
                                        }
                                        break;
                                    }
                                }
                            }, function error(response) {
                                $scope.errors.question_remove[section_id] = response.data.msg;
                            });
                        }
                    } else {
                        console.log('Missing section or question id. Did nothing.');
                    }
                    break;
            }
        };

        /* TODO have flask fill this in from the server? */

        /*
        Functions
         */

        $scope.answer_selected = function(question, answer_id) {
            for (var i = 0; i < question.answers.length; i++) {
                var answer = question.answers[i];
                if (answer.id == answer_id) {
                    return true;
                }
            }
            return false;
        };

        $scope.risk_factor_selected = function(question, risk_factor_id) {
            if (risk_factor_id == question.risk_factors) {
                return true;
            }
            return false;
        };

        /*
        Get all possible answers and risk factors
         */
        var a_api = new ApiCore();
        var answers_promise = a_api.list('answer');
        var risk_factors_promise = a_api.list('risk_factor');
        /*
        Get all questions for this report or nothing if this is an empty (new) report
         */
        var promises = [answers_promise, risk_factors_promise];
        var parse_url = new UrlParse($location.absUrl());
        if (parse_url.has_id === true) {
            var report_promise = a_api.read(parse_url.id, 'report');
            promises.push(report_promise);
        }
        $q.all(promises).then(function success (api_results) {
            var a_convert_answers = new ConvertAnswer(api_results[0]);
            var a_convert_risk_factors = new ConvertRiskFactor(api_results[1]);
            /**
             *
             */
            $scope.available_answers = a_convert_answers.from_api();
            $scope.available_risk_factors = a_convert_risk_factors.from_api();
            if (parse_url.has_id === true) {
                /* Existing report */
                var a_convert_report = new ConvertReport();
                $scope.input_report = a_convert_report.from_api(api_results[2], $scope.available_answers, $scope.available_risk_factors);
                $scope.report = $scope.input_report;
            } else {
                /* New report */
                $scope.report = $scope.report_template;
            }

        });

        /*
        Merge everything into $scope.q_template
         */
        /*
        Create the form
         */
        /*
        var a_api = new ApiCore();
        var api_call = a_api.read(1, 'question');
        $scope.api_call = api_call.get();
        $scope.api_call.$promise.then(function(data) {
            var api_parser = new ConvertQuestion(data);
            $scope.q_template = api_parser.from_api();
            $scope.master = {};
            $scope.submit = function(question) {
                $scope.master = angular.copy(question);
                console.log($scope.master);
            };
            $scope.reset = function() {
                $scope.question = angular.copy($scope.master);
            };
            $scope.init = function() {
                $scope.question = angular.copy($scope.q_template);
            };
            $scope.init();
            console.log($scope.q_template);
        });*/
    }
]);
