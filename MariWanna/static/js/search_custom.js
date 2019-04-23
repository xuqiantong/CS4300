$(document).ready(function(){

    // Autocomplete Options
    let medical_effects = ["Cramps", "Depression", "Eye Pressure", "Fatigue", "Headaches",
        "Inflammation", "Insomnia", "Lack of Appetite", "Muscle Spasms", "Nausea",
        "Pain", "Seizures", "Spasticity", "Stress"];
    let desired_effects = ["Aroused", "Creative", "Energetic", "Euphoric", "Focused", 
        "Giggly", "Happy", "Hungry", "Relaxed", "Sleepy", "Talkative", "Tingly", "Uplifted"];
    let undesired_effects = ["Anxious", "Dizzy", "Dry Eyes", "Dry Mouth", "Headache", "Paranoid"];
    let flavors = ["Apple", "Berry", "Blueberry", "Bubble Gum", "Buttery", "Candy", "Caramel",
        "Cheesy", "Chemical", "Cherry", "Chocolate", "Citrus", "Coffee", "Creamy",
        "Dank", "Diesel", "Flowery", "Fruity", "Grape", "Grapefruit", "Hash",
        "Herbal", "Honey", "Lavender", "Lemon", "Lime", "Mango", "Menthol", "Mint",
        "Nutty", "Orange", "Peppery", "Pine", "Pineapple", "Sage", "Skunky", "Sour",
        "Spicy", "Strawberry", "Sugary", "Sweet", "Tangy", "Tea", "Tobacco",
        "Tropical", "Vanilla", "Woody"];
    let aromas = ["Apple", "Banana", "Berry", "Blueberry", "Bubble Gum", "Candy", "Caramel",
        "Cheese", "Chemical", "Cherry", "Chocolate", "Citrus", "Coffee", "Creamy",
        "Dank", "Diesel", "Earthy", "Floral", "Flowery", "Fragrant", "Fruity", "Fuel",
        "Grape", "Grapefruit", "Grassy", "Harsh", "Hash", "Herbal", "Kush",
        "Lavender", "Lemon", "Lime", "Mango", "Mellow", "Mint", "Musky", "Nutty",
        "Orange", "Pepper", "Pine", "Pineapple", "Pungent", "Sage", "Skunky", "Sour",
        "Spicy", "Strawberry", "Sweet", "Tropical", "Vanilla", "Woody"];
   
    $("#similarSearch").slideDown(500);

    // Effects entry set up
    $('#key-words').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allEffects').append("<p class=\"tag key-word d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-secondary rounded\">" + $(this).val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    });
    $("#key-words-btn").click(function(){
        if ($("#key-words").val() != "") {
            $('#allEffects').append("<p class=\"tag key-word d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-secondary rounded\">" + $("#key-words").val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $("#key-words").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('#medical-effects').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allEffects').append("<p class=\"tag medical-effect d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-primary rounded\">" + $(this).val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    }).autocomplete({
        source: function(request, response) {
            var results = $.ui.autocomplete.filter(medical_effects, request.term);
    
            response(results.slice(0, 5));
        }
    });
    $("#medical-effects-btn").click(function(){
        if ($("#medical-effects").val() != "") {
            $('#allEffects').append("<p class=\"tag medical-effect d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-primary rounded\">" + $("#medical-effects").val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $("#medical-effects").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('#desired-effects').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allEffects').append("<p class=\"tag desired-effect d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-success rounded\">" + $(this).val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    }).autocomplete({
        source: desired_effects,
        max: 5
    });
    $("#desired-effects-btn").click(function(){
        if ($("#desired-effects").val() != "") {
            $('#allEffects').append("<p class=\"tag desired-effect d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-success rounded\">" + $("#desired-effects").val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $("#desired-effects").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('#undesired-effects').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allEffects').append("<p class=\"tag undesired-effect d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-danger rounded\">" + $(this).val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    }).autocomplete({
        source: undesired_effects,
        max: 5
    });
    $("#undesired-effects-btn").click(function(){
        if ($("#undesired-effects").val() != "") {
            $('#allEffects').append("<p class=\"tag undesired-effect d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-danger rounded\">" + $("#undesired-effects").val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $("#undesired-effects").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('#flavors').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allEffects').append("<p class=\"tag flavor d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-info rounded\">" + $(this).val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    }).autocomplete({
        source: flavors,
        max: 5
    });
    $("#flavors-btn").click(function(){
        if ($("#flavors").val() != "") {
            $('#allEffects').append("<p class=\"tag flavor d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light bg-info rounded\">" + $("#flavors").val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $("#flavors").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('#aromas').keypress(function(event) {
        let keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            $('#allEffects').append("<p class=\"tag aroma d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light rounded\">" + $(this).val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    })
    .autocomplete({
        source: aromas,
        max: 5
    });
    $("#aromas-btn").click(function(){
        if ($("#aromas").val() != "") {
            $('#allEffects').append("<p class=\"tag aroma d-inline-flex justify-content-center align-items-center shadow-sm border m-1 pl-2 pr-2 text-small text-light rounded\">" + $("#aromas").val().toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
            $("#aromas").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
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

    let removeX = function(val) {
        return val.substring(0, val.length - 1)
    }
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
        requestData.medicalEffects = [];
        requestData.desiredEffects = [];
        requestData.undesiredEffects = [];
        requestData.flavors = [];
        requestData.aromas = [];
        $("#allEffects").children().each(function(){
            let effect = $(this).text();
            if ($(this).hasClass("medical-effect")) {
                requestData.medicalEffects.push(removeX(effect));
            } else if ($(this).hasClass("desired-effect")) {
                requestData.desiredEffects.push(removeX(effect));
            } else {
                requestData.undesiredEffects.push(removeX(effect));
            }
        });
        $("#allFlavors").children().each(function() {
            let tag = $(this).text();
            if ($(this).hasClass("flavor")) {
                requestData.flavors.push(removeX(tag));
            } else {
                requestData.aromas.push(removeX(tag));
            }
        })
        console.log(requestData);
        $.post( "/results", JSON.stringify(requestData))
        .always(function() {
            $("#loadingDiv").fadeIn();
        })
        .done(function( data ) {
            data = JSON.parse(data);
            
            $('#results').empty();
            // $("#results").children().fadeOut(500, function() {
            //     $('#results').empty();
            // });
            let count = 0;

            data.forEach(function(strain){
                console.log(strain);
                $("#results").append('<div id="strain_'+ count +'" class="card strain-result ml-2 mr-2 mb-2 shadow">' + 
                // '<img src="' + strain[1]["image"] +'" class="card-img-top" alt="...">' +
                '<div class="card-body">' +
                    '<div class="d-flex justify-content-between"><h5 class="card-title font-weight-bolder mb-1">' + strain[1]["name"] +'</h5><p class="text-muted text-small">' + strain[0].toFixed(2) + '</p></div>' +
                        '<p class="card-text mb-1 text-muted font-italic">Rating: '+ Number(strain[1]["rating"]).toFixed(2) +'/5.00</p>' +
                        '<p class="card-text">'+ strain[1]["description"].substring(0, 90) +'...</p>' +
                        '<p class="text-success modal-triggor" data-toggle="modal" data-target="#exampleModalLong">See More</p>' +
                    '</div>' +
                '</div>');
                
                $("#strain_" + count).on("click", function() {
                    $("#modal-name").text(strain[1]["name"]);
                    $("#modal-description").text(strain[1]["description"]);
                    $("#modal-medical").text(strain[1]["medical"]);
                    $("#modal-desired").text(strain[1]["positive"]);
                    $("#modal-undesired").text(strain[1]["negative"]);                    
                    $("#modal-flavors").text(strain[1]["flavors"]);
                    $("#modal-aromas").text(strain[1]["aromas"]);
                });

                count++;
                // $("#results").append('<div class="card strain-result border-0 shadow mb-2"><div class="card-body">' + strain.strain_name + '</div>')
            });
            $("#loadingDiv").fadeOut();

            $("#similarSearch").animate({
                width: "30%"
            }, 500, function(){
                $("#results").addClass("d-flex").show(500);
            });

        });
    });

    
});