/**
 * Created by pieter on 2/06/16.
 */

$(document).ready(function(){
    $('#locale_switcher').find('li').each(function(){
        $(this).find('a').click(function(){
            var locale = $(this).attr('id');
            $.ajax({
                method: 'POST',
                url: '/api/v2/locale/' + locale,
                success: function(data, status) {
                    /* Locale is set server-side */
                    set_js_locale(locale);
                    location.reload(true);
                },
                error: function(jqXHR, status, error) {}
            });
        });
    })
});


function set_js_locale(locale) {
    $.ajax({
        method: 'GET',
        url: '/static/locales/' + locale + '/' + locale + '.json',
        success: function(data, status) {
            $.getScript('/static/locales/' + locale + '/icu.js')
                .done(function(script, textStatus) {
                    _.setTranslation(data);
                });
        },
        error: function(jqXHR, status, error) {
            console.log(error);
        }
    });
}
