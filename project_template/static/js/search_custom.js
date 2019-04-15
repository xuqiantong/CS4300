$(document).ready(function(){
    // Strength slider configuration
    $("#strengthRange").slider({
        value:50,
        min: 0,
        max: 100,
        step: 1,
        slide: function( event, ui ) {
            $( "#strengthValue" ).html( ui.value );
        }
    });
    $( "#strengthValue" ).html(  $('#strengthRange').slider('value') );

    // Effects entry set up
    $('#medical-effects').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allEffects').append("<p class=\"tag  d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-primary rounded\">" + $(this).val() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    });
    $('#desired-effects').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allEffects').append("<p class=\"tag  d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-success rounded\">" + $(this).val() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    });
    $('#undesired-effects').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allEffects').append("<p class=\"tag  d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-danger rounded\">" + $(this).val() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    });

    // Flavors entry set up
    $('#flavors').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allFlavors').append("<p class=\"tag  d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-info rounded\">" + $(this).val() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    });

    // Submit request logic
    $( "#similarSearch" ).submit(function( event ) {
        event.preventDefault();
        $.post( "/results", { 
            data: "John"
        }).done(function( data ) {
            data = JSON.parse(data);
            data.forEach(function(strain){
                console.log(strain);
                $("#results").append('<div class="card strain-result border-0 shadow mb-2"><div class="card-body">' + strain.strain_name + '</div>')
            });
            $("#similarSearch").animate({
                width: "30%"
            }, 500, function(){
                $("#results").show(500);
            });
            
        });
    });

    
});