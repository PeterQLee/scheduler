$(document).ready(function() {
    $("#confpwd").keyup(validate);
});

function validate() {
    var email=$("#regemail").val()
    var password = $("#regpwd").val();
    var confirmPassword = $("#confpwd").val();
    if (!email) {
	Button.disabled=true;
	$("#pwdmsg").text("Enter an email.");
    }
    else if (password != confirmPassword){
	Button.disabled=true;
        $("#pwdmsg").text("Passwords do not match!");
    }
    else {
	Button.disabled=false;
        $("#pwdmsg").text("Passwords match.");
    }

}