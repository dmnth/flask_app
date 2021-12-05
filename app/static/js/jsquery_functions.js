#! /usr/bin/env nodejs

/* Makes selected item toggle slide down animation
 * hides visible elements if present
 */

$(document).ready(function() {
    $('.slide-toggle').click(function(event) {
        var button = $(this)
        var id = button.attr('id')
        var input = $(`#${id}.box`)
        $('.box').each(function() {
            if ($(this).attr('id') != id && $(this).css('display') != 'none') {
                var this_id = $(this).attr('id')
                $(`#${this_id}.box`).animate({height: "toggle"})
            }
        });
        input.animate({ height: "toggle" }, 1000)
    });
});

