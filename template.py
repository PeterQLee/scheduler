
##Prints Headers and links for every page
def printTemplatept1(email):
        print ("""
<html>
<head>
<title>University Scheduler</title>
<link rel="stylesheet" href="SchedulerStyle.css">
</head>

<body>
<!-- random stuff and links-->
<p align="right">Currently logged in as: %s</p>
<ul id="Menu">
<li><a href="index.py">Home</a></li>
<li><a href="selectcourses.py">Select Courses</a></li>
<li><a href="calander.py">Make your schedule</a></li>
<li><a href="viewoption.py">Selection Options</a></li>
<li><a href="logout.py">Logout</a></li>
<li><a href="help.html">Help</a></li>
</ul>
</br>
</br>
</br>
</br>

"""%email)
def printTemplatept2():
        print ("""
</body>
</html>""")
    

