/**
 * Created by pieter on 5/01/16.
 */

var UrlParse = function(url) {
    this.url = url;
    this.has_id = false;
    this.id = this.get_id();
    this.type = this.get_type();
};

UrlParse.prototype.get_id = function() {
    /**
     * Get the ID from the server-provided field, and set this.has_id to true. Return null otherwise.
     */
    return this.get_str_id('report_id');
};

/**
 * Get the str_id, which is the ID of an input type somewhere on the page.
 * @param str_id
 */
UrlParse.prototype.get_str_id = function(str_id) {
    var id = document.getElementById(str_id).getAttribute('value');
    if (id === null) {
        console.log('Error: no id provided');
        return null;
    } else {
        this.has_id = true;
        return id;
    }
};

UrlParse.prototype.get_type = function() {
    return 'report';
};
