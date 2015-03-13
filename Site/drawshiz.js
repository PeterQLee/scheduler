
var re=[1];

function sortdat(lit) {
    
    //console.log(lit);
    var bist=lit;
    if (bist.length==1) {
	return bist;
    }
    var piv=bist[Math.floor(bist.length/2)];
    bist.splice(Math.floor(bist.length/2),1);
    
    var less=[]
    var more=[]//list.slice(list.length/2,list.length-1);
    //console.log(bist);
    for (var i=0;i<bist.length;i++) {
	if (Math.abs(piv)>=Math.abs(bist[i])) {
	    less.push(bist[i]);
	}
	else {
	    more.push(bist[i]);
	}
    }
    if (less.length>0)
	less=sortdat(less);
    //console.log(less);
    if (more.length>0)
	more=sortdat(more);
    //console.log(more);
    var n=[piv];//concat(less,[piv]);
    var fin=less.concat(n,more);
    return fin;
    
}
function draw() {
    console.log("ER")
    var xofset=50;
    var yofset=50;
    //data=[[1,"TEST",100,200]]
    var checke=[]
    var names=[]
    var coords=[]
    for (var i=0;i<data.length;i++) {
	if ($("#"+data[i][0].toString()).is(':checked')) {
	    tpcords=[]
	    names.push(data[i][1]+": "+data[i][0].toString());
	    for (var j=2;j<data[i].length;j+=2) {
		
		checke.push(data[i][j]);
		checke.push(-1*data[i][j+1]); //neg end points
		tpcords.push((Math.floor(data[i][j]/2400))*100);
		tpcords.push((Math.floor((data[i][j]%2400)/100)*60)+(data[i][j]%100));
	    }
	    coords.push(tpcords);
	    
	}
    }
    //console.log(checke);
    checke=sortdat(checke);
    //console.log(checke);
    //look for overlap
    
    var blue=[];
    var red =[];
    var poscount=0;
    var startpt=0;
    for (var i=0;i<checke.length;i++) {
	var posflag=false;
	if (checke[i]>=0) {
	    poscount+=1;
	    posflag=true;
	}
	else {
	    poscount-=1;
	}
	if (poscount==1 && posflag) {
	    startpt=Math.abs(checke[i]);
	}
	if (poscount==2 && posflag) {
	    blue.push(startpt);
	    blue.push(Math.abs(checke[i]));
	    startpt=Math.abs(checke[i]);
	}
	if (poscount==1 && !posflag) {
	    red.push(startpt);
	    red.push(Math.abs(checke[i]));
	    startpt=Math.abs(checke[i]);
	}
	if (poscount==0) {
	    blue.push(startpt);
	    blue.push(Math.abs(checke[i]));
	}
    }
    //console.log(blue);
    //console.log(red);
	
	    
    var elem=$('#calapp')[0];
    var context=elem.getContext('2d');
    context.clearRect(0,0,550,1500);
    context.fillStyle="#0000FF";
    for (var i=0;i<blue.length;i+=2) {
	
	
	var xcord=(Math.floor(blue[i]/2400))*100;
	var ycord1=(Math.floor((blue[i]%2400)/100))*60+(blue[i]%100);
	var ycord2=(Math.floor((blue[i+1]%2400)/100))*60+(blue[i+1]%100)-ycord1;
	context.fillRect(xcord+xofset,ycord1+yofset,100,ycord2);
	//console.log(xcord);
	//console.log(ycord1);
	//console.log(ycord2);
    }

    for (var i=0;i<red.length;i+=2) {
	context.fillStyle="#FF0000";
	var xcord=(Math.floor(red[i]/2400))*100;
	var ycord1=(Math.floor((red[i]%2400)/100))*60+(red[i]%100);
	var ycord2=(Math.floor((red[i+1]%2400)/100))*60+(red[i+1]%100)-ycord1;
	context.fillRect(xcord+xofset,ycord1+yofset,100,ycord2);
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
    context.font="bold 12px sans-serif";
    for (var i=0;i<=1440;i+=60) {
	context.fillText(Math.floor(i/60).toString()+"00-",0,i+yofset+4);
    }
    var dayz=["Monday","Tuesday","Wednesday","Thursday","Friday"];
    for (var i=0;i<500;i+=100) {
	context.fillText(dayz[Math.floor(i/100)],i+xofset+10,30);
    }
    //context.fillRect(0,50,100,100);
    console.log(names);
    context.fillStyle="#00FF00";
    for (var i=0;i<names.length;i++) {
	for (var j=0;j<coords[i].length;j+=2) {
	    context.fillText(names[i],coords[i][j]+xofset+10,coords[i][j+1]+yofset+10);
	}
    }
}