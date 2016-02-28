$(document).ready(function() {
    $("#confpwd").keyup(validate);
    $("#regemail").keyup(check_email);
});
var tabval=9;
var emflag=false;
var butflag=false;
function validate() {
    

    var password = $("#regpwd").val();
    var confirmPassword = $("#confpwd").val();
    //if (key==tabval)
//	check_email();
    
    if (password != confirmPassword ) {
	Button.disabled=true;
        $("#pwdmsg").text("Passwords do not match!");
	butflag=false;
    }
    else {
	if (emflag) {
	    Button.disabled=false;
            $("#pwdmsg").text("");
	}
	else {
	    $("#pwdmsg").text("Handle is not unique or invalid.");
	}
	    
	butflag=true;
    }
    
}
function check_email() {
    var email=$("#regemail").val();
    if (butflag) {
	$.ajax({dataType:"json",url:"checklogin.py?email="+email,mimeType:"text/plain",success:function(data) {
	//Only do this on mouse move (or tab)
	    

	
	if (!email || data  ) {
	//check uniqueness
	    Button.disabled=true;
	    $("#pwdmsg").text("Handle is not unique or invalid.");
	    emflag=false;
	}
	else {
	    Button.disabled=false;
	    emflag=true;
	    $("#pwdmsg").text("");
	}


    }});
    }
}