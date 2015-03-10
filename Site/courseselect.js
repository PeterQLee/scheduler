$(document).ready(function(){
    $("#end_time").keyup(timeEnter);
    $("#start_time").keyup(timeEnter);
    $("#cname").keyup(timeEnter);
    $("#M").change(timeEnter);
    $("#T").change(timeEnter);
    $("#W").change(timeEnter);
    $("#R").change(timeEnter);
    $("#F").change(timeEnter);
});
//make sure at least one day of week is selected
//make sure times are valid too
function timeEnter() {
    var start=$("#start_time").val();
    var end=$("#end_time").val();
    var regex= /[0-9]/;
    var cname=$("#cname").val();
    var Mflag=$("#M").is(':checked');
    var Tflag=$("#T").is(':checked');
    var Wflag=$("#W").is(':checked');
    var Rflag=$("#R").is(':checked');
    var Fflag=$("#F").is(':checked');
    var numst=parseInt(start);
    var numend=parseInt(end);
    if (start.length!=4 || end.length!=4 || !regex.test(start)||!regex.test(end)||cname.length==0){
	addcourse.disabled=true;
	$("#feedback").text("Make sure time slots are 4 digit and numeric");
    }
    
    else if (numst>=2400 || numend>=2400|| numst>=numend||numst%100>=60 || numend%100>=60) {
	addcourse.disabled=true;
	$("#feedback").text("Make sure time slots are valid");
    }
    else if (!Mflag && !Tflag &&!Wflag && !Rflag && !Fflag) {
	addcourse.disabled=true;
	$("#feedback").text("Select at least one day");
    }
	
    else {
	addcourse.disabled=false;
	$("#feedback").text("Course is VALID");
    }
}