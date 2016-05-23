/**
 * Created by pieter on 23/05/16.
 */

function success_button(message) {
    return('<button type="button" class="btn btn-success">' + message + '</button>');
}

function error_button(message) {
    return('<button type="button" class="btn btn-danger">' + message + '</button>');
}

function save_button(message) {
    return default_button(message);
}

function default_button(message) {
    return ('<button type="button" class="btn btn-default">' + message + '</button>');
}