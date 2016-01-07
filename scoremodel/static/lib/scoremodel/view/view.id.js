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
     * Get the ID from the URL, and set this.has_id to true. Return null otherwise.
     */
    var id_patt = /\/id\/([0-9]+)\/?/i;
    var id_loc = this.url.match(id_patt);
    if (id_loc != null) {
        this.has_id = true;
        return id_loc[1];
    }
    return null;
};

UrlParse.prototype.get_type = function() {
    /**
     * Get the type of item (e.g. question) from the URL and return it or null.
     * This is also the endpoint of the API
     */
    var type_patt = /\/type\/(.*?)\//i; /* TODO what if the url is like /type/foo ? */
    var type_loc = this.url.match(type_patt);
    if (type_loc != null) {
        return type_loc[1];
    } else {
        console.log('Error: no type provided.');
        return null;
    }
};
