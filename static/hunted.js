
function enterAction(e) {
    e.preventDefault();
}

$(document).ready(function() {
    $("input[type='submit']").click(enterAction);
    $("#action-input").focus();    
});