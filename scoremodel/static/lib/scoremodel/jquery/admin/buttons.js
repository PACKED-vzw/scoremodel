/**
 * Created by pieter on 23/05/16.
 */

function success_button(selector, message) {
    $(selector)
        .attr('class', 'btn btn-success')
        .text(message);
}

function error_button(selector, message) {
    $(selector)
        .attr('class', 'btn btn-danger')
        .text(message);
}

function default_button(selector, message) {
    $(selector)
        .attr('class', 'btn btn-default')
        .text(message);
}

