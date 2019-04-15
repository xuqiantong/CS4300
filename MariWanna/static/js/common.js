$(document).ready(function(){
    var height = $(window).height();

    let nav_height = $("nav").height();
    
    $("#mainContent").css("min-height", height-nav_height);


    $(window).resize( function() {
        $("#mainContent").css("height", $(window).height() - nav_height);
    });
})