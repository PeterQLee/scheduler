var context=null;
var lincontext=null;
var boxes=[]; //state, xcord, ycord, yfin
var bcolours=["#0000FF","#22FFFF"];

var dragFlag=false;
var dragLocx=-1;
var dragLocy=-1;
var dragIndex=-1;
var dragDirect=0;
var xmargin=50;
var ymargin=50;
$(function() {
	var elem=$('#calapp')[0];
	var e=$('#calapp2')[0];
	context=elem.getContext('2d');
	lincontext=e.getContext('2d');
	e.addEventListener('mousemove',function(e){
	    	respondMove(context,boxes,e);
	    });
	e.addEventListener("mousedown",function(e){
		respondDrag(boxes,e);
	    });
	e.addEventListener("mouseup",function(e){
		releaseMouse(boxes,e);
	    });

	
    
    }); 

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
    var xscale=100;
    var yscale=60;

    var xofset=50;
    var yofset=50;
    //data=[[1,"TEST",100,200]]
    var checke=[]
    var names=[]
    var coords=[]
    for (var i=0;i<data.length;i++) {

	    tpcords=[]
	    names.push(data[i][1]+": "+data[i][0].toString());
	    for (var j=2;j<data[i].length;j+=2) {
		
		checke.push(data[i][j]);
		checke.push(-1*data[i][j+1]); //neg end points
		tpcords.push((Math.floor(data[i][j]/2400))*100);
		tpcords.push((Math.floor((data[i][j]%2400)/100)*60)+(data[i][j]%100));
		boxes.push(0);
		boxes.push(Math.floor(data[i][j]/2400)*xscale);
		//boxes.push(Math.floor(data[i][j]%2400)/100)*yscale);
		var ycord1=(Math.floor((data[i][j]%2400)/100))*yscale+(data[i][j]%100);
		boxes.push(ycord1);
		boxes.push(Math.floor((data[i][j+1]%2400)/100)*yscale+(data[i][j+1]%100));
	    //state,x1,y1,x2,y2
	    }
	    coords.push(tpcords);
	    
	    //}
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
	    

    

    
    var rad=12;

    context.clearRect(0,0,550,1500);
    context.fillStyle="#0000FF";
    for (var i=0;i<blue.length;i+=2) {
	
	
	var xcord=(Math.floor(blue[i]/2400))*100;
	var ycord1=(Math.floor((blue[i]%2400)/100))*60+(blue[i]%100);
	var ycord2=(Math.floor((blue[i+1]%2400)/100))*60+(blue[i+1]%100)-ycord1;
	
	drawBubbleRect(context,xcord+xofset,ycord1+yofset,100,ycord2,12,3,"#0000FF");
	//context.fillRect(xcord+xofset,ycord1+yofset,100,ycord2);
	

    }

    for (var i=0;i<red.length;i+=2) {
	context.fillStyle="#FF0000";
	var xcord=(Math.floor(red[i]/2400))*100;
	var ycord1=(Math.floor((red[i]%2400)/100))*60+(red[i]%100);
	var ycord2=(Math.floor((red[i+1]%2400)/100))*60+(red[i+1]%100)-ycord1;
	//context.fillRect(xcord+xofset,ycord1+yofset,100,ycord2);
	drawBubbleRect(context,xcord+xofset,ycord1+yofset,100,ycord2,12,3,"#0000FF");
    }

    //console.log(names);
    context.fillStyle="#00FF00";
    for (var i=0;i<names.length;i++) {
	for (var j=0;j<coords[i].length;j+=2) {
	    textInPlace(names[i],coords[i][j]+xofset+10,coords[i][j+1]+yofset+10,context)
	    //context.fillText(names[i],coords[i][j]+xofset+10,coords[i][j+1]+yofset+10);
	}
    }
}

function redrawRegion(state,xcord,ycord,height){

    //clears a given rect in context and redraws with the given parameters
    var xofset=50;
    var yofset=50;
    context.clearRect(xofset+xcord,yofset+ycord,100,height);

    drawBubbleRect(context,xcord+xofset,ycord+yofset,100,height,12,3,bcolours[state]);
    
}
function initdraw(){
    var xofset=50;
    var yofset=50;


    //Lines
    lincontext.fillStyle="#0000FF";
    for (var i=0;i<=1440;i+=30) {
	lincontext.beginPath();
	lincontext.moveTo(xofset,i+yofset);
	lincontext.lineTo(500+xofset,i+yofset);
	lincontext.closePath();
	lincontext.stroke();
    }
    for (var i=0;i<=500;i+=100) {
	lincontext.beginPath();
	lincontext.moveTo(i+xofset,yofset);
	lincontext.lineTo(i+xofset,1440+yofset);
	lincontext.closePath();
	lincontext.stroke();
    }
        //draw in names
    lincontext.font="bold 9px sans-serif";
    for (var i=0;i<=1440;i+=60) {
	lincontext.fillText(Math.floor(i/60).toString()+"00-",0,i+yofset+4);
    }
    var dayz=["Monday","Tuesday","Wednesday","Thursday","Friday"];
    for (var i=0;i<500;i+=100) {
	lincontext.fillText(dayz[Math.floor(i/100)],i+xofset+10,30);
    }
    //context.fillRect(0,50,100,100);

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

function respondMove(context,boxes,e) {
    if (dragFlag) {
	context.clearRect(xmargin+boxes[dragIndex+1],ymargin+boxes[dragIndex+2],100,boxes[dragIndex+3]-boxes[dragIndex+2]);

	respondDrag(boxes,e);
	redrawRegion(boxes[dragIndex],boxes[dragIndex+1],boxes[dragIndex+2],boxes[dragIndex+3]-boxes[dragIndex+2]);
	return;
    }


    var xcord=e.pageX;//-xmargin;
    var ycord=e.pageY;//-ymargin;
    //    console.log(xcord);
    //console.log(ycord);
    //console.log(boxes);
    for (var i=0;i<boxes.length;i+=4) {
	//check collision
	x1=boxes[i+1]+xmargin;
	y1=boxes[i+2]+ymargin;
	y2=boxes[i+3]+ymargin;
	if (boxes[i]==0 ){
	    if (xcord>x1 && xcord<(x1+100)) {
		if (ycord>y1 && ycord<y2) {
		    //console.log(xcord,ycord,x1,y1,y2);
		    boxes[i]=1;
		    redrawRegion(1,boxes[i+1],boxes[i+2],boxes[i+3]-boxes[i+2]);

		}
		
	    }
	}
	if (boxes[i]==1) {
	    if (xcord<x1 || xcord>(x1+100)|| ycord<y1 || ycord>y2) {
		
		boxes[i]=0;
		redrawRegion(0,boxes[i+1],boxes[i+2],boxes[i+3]-boxes[i+2]);

			       
	    }
	}
	
    }

    /*
      Basically responds to mouse movement to give boxes asthetic highlighting
     */
    
}
function respondDrag(boxes,e) {
    console.log("DRAG");
    //resize/make new thuing
    var clickmargin=25;
    //(add marginx/y to thing
    var x=e.pageX-xmargin;
    var y=e.pageY-ymargin;
    
    if (!dragFlag) {
	//first time pressing mouse down
	dragLocx=x;
	dragLocy=y;
	//check boundaries of all things
	for (var i=0;i<boxes.length;i+=4) {
	    var y1=boxes[i+2];
	    var y2=boxes[i+3];
	    if (Math.floor(x/100)*100==boxes[i+1] && y>y1 && y<y1+clickmargin) {
		//dragging up
		dragIndex=i;
		dragDirect=-1;
		break;
	    }
	    
	    else if (Math.floor(x/100)*100==boxes[i+1] && y>y2-clickmargin && y <y2) {
		dragIndex=i;
		dragDirect=1;
		break;
	    }

	}
	if (dragDirect==0) {
	    //no direction, hence create new box
	    dragIndex=boxes.length;
	    boxes.push(1);
	    boxes.push(Math.floor(dragLocx/100)*100);
	    boxes.push(dragLocy);
	    boxes.push(dragLocy);
	}
	else {
	    console.log("RESIZE");
	}
	
    }
    else {
	//already dragging something
	var y1=boxes[dragIndex+2];
	var y2=boxes[dragIndex+3];
	
	if (y>y1) {
	    boxes[dragIndex+3]=y;
	}
	else {
	    boxes[dragIndex+2]=y;
	}
	
    }
    
    dragLocx=x;
    dragLocy=y;   
    console.log("DO");
    dragFlag=true;
}
function releaseMouse(boxes,e) {
    console.log("REL");
    if (dragFlag) {
	dragFlag=false;
	var x=e.pageX;
	var y=e.pageY;
	var marginX=50;
	var marginY=50;
	
	//TODO: call a merging function, merges all overlapping things
	mergeBox();
	redrawRegion(boxes[dragIndex],boxes[dragIndex+1],boxes[dragIndex+2],boxes[dragIndex+3]-boxes[dragIndex+2]);
	dragIndex=-1;
	dragDirect=0;
	dragLocx=-1;
	dragLocy=-1;
	console.log("RELEAS");
    }

}
function mergeBox(){
    //merges current Index
    var remove=[];
    
    for (var i=0;i<boxes.length;i+=4) {
	if (i==dragIndex  ) continue;
	
	//check overlap
	if (overlap(boxes[i+1],boxes[dragIndex+1],boxes[dragIndex+2],boxes[dragIndex+3],boxes[i+2],boxes[i+3])) {
	    //overlapping boxes, set to i and delete dragIndex
	    var y1=Math.min(boxes[dragIndex+2],boxes[i+2]);
	    var y2=Math.max(boxes[dragIndex+3],boxes[i+3]);

	    boxes[dragIndex+2]=y1;
	    boxes[dragIndex+3]=y2;

	    console.log(boxes,i,dragIndex);
	    remove.push(i);
	    //dragIndex=i;

	    
	}
		    
    }
    for (var i=0;i<remove.length;i++) {
	boxes.splice(remove[i],4);
    }

}
function overlap(x1,x2,y1,y2,y3,y4) {
    if (Math.floor(x1/100)==Math.floor(x2/100)) {
	if (y1>y3 && y1<y4) {
	    //first coord is in
	    return true;
	}
	if (y2>y3 && y2<y4) {
	    //second coord is in
	    return true;
	}
	
	if (y3>y1 && y3<y2) {
	    //third coord is in
	    return true;
	}
	
	if (y4>y1 && y4<y2) {
	    //fourth coord is in
	    return true;
	}

    }
    return false;
}

