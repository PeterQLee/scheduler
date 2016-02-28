#
def redirect():#cookid):
    #redirects user back to index page
    s="""
<html>
<head>
<title>NO CREDS BRO</title>
</head>

<body>
   <script type="text/JavaScript">
      window.location="index.py"
   </script>

   <a href="index.py"> Login Credentials Expired</a>

</body>

</html>
"""
    return s
