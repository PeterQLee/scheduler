#prints html for the login page
def LoginPage(args):
    print ("""
<html>
<head>

	<title>University Scheduler</title>
	<link rel="stylesheet" href="SchedulerStyle.css">
	
	
</head>

<body>
	<ul id="Menu">
<li><a href="index.py">Home</a></li>
<li><a href="help.html">Help</a></li>
</ul>
	<br><br><br>
	
	<h2>About University Scheduler</h2>
	<p>University Scheduler is a site design to help you, the user, make an ideal timetable for your College
	or University. No matter where you are attending, this site will help you design a schedule fit for your
	desires and needs.</p>
	<br>
	<table id="Login" style="background-color:#FFC338" align="left" border="3" cellpadding="100">
		<tr cols=1>
			<td>
	<h3 align="center">Login Required</h3>
	<form action="login.py" method="post">
	<p align="center">Email: <input type= "text" size="30" name="loginemail"></p>
	<p align="center">Password: <input type= "password" size="25" name="loginpass"></p>
	<p align="center"><input type="submit" value="Login"></p>
	</form>
	</td>
	</tr>
	</table>

	
	
	<table id="Sign-Up" style="background-color:#FFC338" align="right" border="3" cellpadding="85">
		<tr cols=1>
			<td>
	<h3 align="center">Sign-Up</h3>
	<form action="register.py" method="post">
	<p align="center">Email: <input type= "text" size="30" name="regemail" id="regemail"></p>
	<p align="center">Password: <input type= "password" size="25" name="regpwd" id="regpwd"></p>
	<p align="center">Confirm Password: <input type= "password" size="16" name="confpwd" id="confpwd"></p>
	<p align="center"><input type="submit" value="Register" id="Button" disabled></p>
	</form>
	<p id="pwdmsg"></p>
	</td>
	</tr>
	</table>
	<br><br>
	<script type="text/javascript" src="jquery-1.10.2.js">
	</script>
	<script type="text/javascript" src="./checkpwd.js">
	</script>

""")
    if "success" in args:
        print ("<p>Registration Successful!!</p>")
    if "incorrect" in args:
        print ("<p>Incorrect Password!</p>")
    print ("""
</body>

</html>

""")
