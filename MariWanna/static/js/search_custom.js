$(document).ready(function(){
    
    // Effects entry set up
    $('#medical-effects').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allEffects').append("<p class=\"tag medical-effect d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-primary rounded\">" + $(this).val() + "<span class=\"remove-btn\">x</span></p>");
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
            $('#allEffects').append("<p class=\"tag desired-effect d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-success rounded\">" + $(this).val() + "<span class=\"remove-btn\">x</span></p>");
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
            $('#allEffects').append("<p class=\"tag undesired-effect d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-danger rounded\">" + $(this).val() + "<span class=\"remove-btn\">x</span></p>");
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
            $('#allFlavors').append("<p class=\"tag flavor d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-info rounded\">" + $(this).val() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    });

    $('#aromas').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allFlavors').append("<p class=\"tag aroma d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light rounded\">" + $(this).val() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    });

    // Strength slider configuration
    $("#strengthRange").slider({
        value:50,
        min: 0,
        max: 100,
        step: 1,
        slide: function( event, ui ) {
            $( "#strengthValue" ).html( ui.value );
            requestData.strength = ui.value;
        }
    });
    $( "#strengthValue" ).html(  $('#strengthRange').slider('value') );

    let requestData = {};
    requestData.medicalEffects = [];
    requestData.desiredEffects = [];
    requestData.undesiredEffects = [];
    requestData.flavors = [];
    requestData.aromas = [];
    requestData.city = "";
    requestData.state = "";
    
    $("#city").on("change", function() {
        requestData.city = $(this).val();
    });

    $("#state").on("change", function() {
        requestData.state = $(this).val();
    });
    
 $("#state")[0].value;

    // Submit request logic
    $( "#similarSearch" ).submit(function( event ) {
        event.preventDefault();
        $("#allEffects").children().each(function(){
            let effect = $(this).text();
            if ($(this).hasClass("medical-effect")) {
                requestData.medicalEffects.push(effect);
            } else if ($(this).hasClass("desired-effect")) {
                requestData.desiredEffects.push(effect);
            } else {
                requestData.undesiredEffects.push(effect);
            }
        });
        $("#allFlavors").children().each(function() {
            let tag = $(this).text();
            if ($(this).hasClass("flavor")) {
                requestData.flavors.push(tag);
            } else {
                requestData.aromas.push(tag);
            }
        })
        console.log(requestData);
        $.post( "/results", requestData)
        .done(function( data ) {
            data = JSON.parse(data);
            $("#results").empty();
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