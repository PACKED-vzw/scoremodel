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
    var id = document.getElementById('report_id').getAttribute('value');
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
