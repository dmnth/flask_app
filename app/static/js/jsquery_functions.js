#! /usr/bin/env nodejs

$(document).ready(function() {
    $('.slide-toggle').click(function(event) {
        var clicked = $(this)
        var id = clicked.attr('id')
        $(`#${id}.box`).animate({ height: "toggle" })
    });
});





/*
$(document).ready(function(){
    var clicked = $(this)
    console.log(clicked)
    $('.slide-toggle').each(function() {
        $(this).click( function(){
            if ($(this) == clicked)
            $('.box').each(function() {
                $(this).animate({ height: "toggle"})
            });
        });
    });
});
*/
/*
$(document).ready(function(){
  $(".slide-toggle-1").click(function(){
    $("#1").animate({
      height: "toggle"
    });
  });
});

$(document).ready(function(){
  $(".slide-toggle-2").click(function(){
    $("#2").animate({
      height: "toggle"
    });
  });
});
*/
