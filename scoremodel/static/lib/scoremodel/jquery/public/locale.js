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
                    location.reload(true);
                },
                error: function(jqXHR, status, error) {}
            });
        });
    })
});
