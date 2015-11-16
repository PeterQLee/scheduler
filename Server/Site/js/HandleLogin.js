
//var email=document.getElementByID('retEmail').value;
//var pass=document.getElementByID('retPass').value;

var c= require('mongodb').MongoClient;
var db=conn.getDB("unisq");

var n=db.Users.find({"email":"leep1995@gmail.com"})

if (n.length ==0 ) {
    document.write("NOPE");
}
else {
    document.write("YEP");
}

