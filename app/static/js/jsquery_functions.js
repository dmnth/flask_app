#! /usr/bin/env nodejs

$(document).ready(function(){
  $(".slide-toggle").click(function(){
    $(".box").animate({
      width: "toggle"
    });
  });
});
