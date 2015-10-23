$(document).ready(function(){
    $("#sel-list").change(draw);
    draw();
});

function draw() {
    var optionnum=$("#sel-list")[0].selectedIndex;
    console.log("DRAW"+optionnum)
    $.ajax({dataType:"json",url:"optiondata.py?pnum="+optionnum,mimeType:"text/plain",success:function(data) {
	console.log(data)
	var xofset=50;
	var yofset=50;
    
	var elem=$('#calapp')[0];
	var context=elem.getContext('2d');
	context.clearRect(0,0,550,1500);
	context.fillStyle="#0000FF"
  
	names=[]
	coords=[]
	for (var i=0;i<data.length;i++) {
	    tpcords=[]
	    for (var j=2;j<data[i].length;j+=2) {
		var xcord=(Math.floor(data[i][j]/2400))*100;
		var ycord1=(Math.floor((data[i][j]%2400)/100)*60)+(data[i][j]%100);
		var ycord2=(Math.floor((data[i][j+1]%2400)/100)*60)+(data[i][j+1]%100)-ycord1;
		context.fillRect(xcord+xofset,ycord1+yofset,100,ycord2);
		tpcords.push(xcord);
		tpcords.push(ycord1);
	    }
	    names.push(data[i][1]+": "+data[i][0].toString());
	    coords.push(tpcords);
	}
	for (var i=0;i<=1440;i+=30) {
	    context.beginPath();
	    context.moveTo(xofset,i+yofset);
	    context.lineTo(500+xofset,i+yofset);
	    context.closePath();
	    context.stroke();
	}
	for (var i=0;i<=500;i+=100) {
	    context.beginPath();
	    context.moveTo(i+xofset,yofset);
	    context.lineTo(i+xofset,1440+yofset);
	    context.closePath();
	    context.stroke();
	}
	context.font="bold 9px sans-serif";
	for (var i=0;i<=1440;i+=60) {
	    context.fillText(Math.floor(i/60).toString()+"00-",0,i+yofset+4);
	}
	var dayz=["Monday","Tuesday","Wednesday","Thursday","Friday"];
	for (var i=0;i<500;i+=100) {
	    context.fillText(dayz[Math.floor(i/100)],i+xofset+10,30);
	}
	    context.fillStyle="#00FF00"
	for (var i=0;i<names.length;i++) {
	    for (var j=0;j<coords[i].length;j+=2) {
		textInPlace(names[i],coords[i][j]+xofset+10,coords[i][j+1]+yofset+10,context);
	    }
	}
    }});
    
}
function textInPlace(name,xstart,ystart,context) {
    var totlen=name.length;
    var increment=10;
    var heightspacing=10;
    var i;
    for (i=0;i<totlen/increment-1;i++) { //fills in text with appopriate spacing
	var k=name.substring(i*increment,(i+1)*increment);
	
		context.fillText(k,xstart,ystart+heightspacing*i);
    }
    context.fillText(name.substring(i*increment,totlen),xstart,ystart+heightspacing*i);
}
