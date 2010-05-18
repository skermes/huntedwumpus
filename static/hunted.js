
function enterAction(e) {
    var action = $("#action-input").val()
    
    if (action == "s" || action == "m")
    {
        e.preventDefault();
        
        if (action == "s")
            $("label[for='argument-input']").text("How long?");
        else
            $("label[for='argument-input']").text("Where to?");
            
        $("#argument-input").focus();
    }    
}

$(document).ready(function() {
    $("#enter").click(enterAction);
    $("#action-input").focus();        
});