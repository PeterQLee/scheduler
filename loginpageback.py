
def LoginPage(args):
    print ("""
<html>
<head>

</head>

<body>

<form action="login.py" method="post">
  <p>Email</p><input type="text" name="loginemail">
  <p>Password</p><input type="password" name="loginpass">
  <input type="submit"  value="Login">
</form>

<form action="register.py" method="post" >
  <p>Email</p><input type="text" name="regemail" id="regemail">
  <p>Password</p><input type="password" name="regpwd" id="regpwd">
  <p>Confirm Password</p> <input type="password" name="confpwd" id="confpwd">
  <input type="submit" value="Register" id="Button" disabled>
</form>

<p id="pwdmsg"></p>

<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js">
</script>
<script type="text/javascript" src="./checkpwd.js">
</script>
<!-- when registering, use js to check if passwords match-->
""")
    if "success" in args:
        print ("<p>Registration Successful!!</p>")
    if "incorrect" in args:
        print ("<p>Incorrect Password!</p>")
    print ("""
</body>

</html>

""")
