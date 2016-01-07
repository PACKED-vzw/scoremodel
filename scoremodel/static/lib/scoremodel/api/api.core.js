/**
 * Created by pieter on 5/01/16.
 */

var api_core = angular.module('scoremodel.api_core', ['ngResource']);

api_core.factory('ApiCore', ['$resource', '$http',
    function($resource, $http){
        var ApiCore = function() {
            /**
             * This class contains the functions (warning: asynchronous!) for API calls. It does no data
             * validation or the like, so the input data must be correct. It does however convert it to
             * JSON.
             * The endpoint variable is everything in the URL of the API between this.url and the ID (if any).
             * E.g. if the URL of the API is http://localhost:5000/api/section/1; then
             *      http://localhost:5000/api/ is this.url
             *      section is the endpoint
             *      1 is the ID
             * It returns the $resource or $http object, depending on the call.
             */
            this.url = 'http://localhost:5000/api/';
            this.http_config = {
                headers: {
                    'Content-Type': 'application/json'
                }
            };
        };

        ApiCore.prototype.mk_url = function(endpoint, object_id) {
            if(object_id === null) {
                return this.url + endpoint;
            } else {
                return this.url + endpoint + '/' + object_id;
            }
        };

        ApiCore.prototype.create = function(data, endpoint) {
            var api_url = this.mk_url(endpoint, null);
            var api_data = JSON.stringify(data);
            //var api_data = data;
            return $http.post(api_url, api_data, this.http_config);
        };

        ApiCore.prototype.read = function(object_id, endpoint) {
            var api_url = this.mk_url(endpoint, object_id);
            return $http.get(api_url);
        };

        ApiCore.prototype.update = function(object_id, data, endpoint) {
            var api_url = this.mk_url(endpoint, object_id);
            var api_data = JSON.stringify(data);
            //var api_data = data;
            return $http.put(api_url, api_data, this.http_config);
        };

        ApiCore.prototype.delete = function(object_id, endpoint) {
            var api_url = this.mk_url(endpoint, object_id);
            return $http.delete(api_url, this.http_config);
        };

        ApiCore.prototype.list = function(endpoint) {
            var api_url = this.mk_url(endpoint, null);
            return $http.get(api_url);
        };

        return ApiCore;
    }]);
