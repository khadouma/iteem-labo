$("#contactForm").validator().on("submit", function (event) {
    if (event.isDefaultPrevented()) {
        // handle the invalid form...
        formError();
        submitMSG(false, "Did you fill in the form properly?");
    } else {
        // everything looks good!
        event.preventDefault();
        submitForm();
    }
});

function submitForm(){
    // Initiate Variables With Form Content
    var name = $("#name").val();
    var email = $("#email").val();
    var number = $("#number").val();
    var message = $("#message").val();
    var csrf_token = $("input[name='csrfmiddlewaretoken']").val(); // Get the CSRF token

    $.ajax({
        type: "POST",
        url: "/send_email/",  // Use the Django URL for sending email
        data: {
            'csrfmiddlewaretoken': csrf_token,
            'name': name,
            'email': email,
            'number': number,
            'message': message
        },
        success : function(response){
            if (response.message === "Email sent successfully"){
                formSuccess();
            } else {
                formError();
                submitMSG(false, response.message);
            }
        }
    });
}

function formSuccess(){
    $("#contactForm")[0].reset();
    submitMSG(true, "Message Submitted!");
}

function formError(){
    $("#contactForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
        $(this).removeClass();
    });
}

function submitMSG(valid, msg){
    if(valid){
        var msgClasses = "h3 text-center tada animated text-success";
    } else {
        var msgClasses = "h3 text-center text-danger";
    }
    $("#msgSubmit").removeClass().addClass(msgClasses).text(msg);
}
