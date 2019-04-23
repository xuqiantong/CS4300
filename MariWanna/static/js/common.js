$(document).ready(function(){
    var height = $(window).height();

    let nav_height = $("nav").height();
    
    $("#mainContent").css("min-height", height-nav_height);

    $('#loader')
    // .hide()  // Hide it initially
    .ajaxStart(function() {
        $(this).show();
    })
    .ajaxStop(function() {
        $(this).hide();
    })
;

    $(window).resize( function() {
        $("#mainContent").css("min-height", $(window).height() - nav_height);
    });
})