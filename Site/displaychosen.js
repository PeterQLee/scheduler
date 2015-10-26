

$("#tags").submit(function(event) {
    console.log( $( this ).serializeArray()[3] );
    var arr=$( this ).serializeArray();
    var tags="";
    var seas="";
    for (var i=0;i<arr.length;i++) {
	if (arr[i]["name"]=="season") seas=arr[i]["value"];
	tags+="tag="+(arr[i]["value"])+"&";
	
    }
    console.log(tags);
    console.log(seas);
    $.ajax({dataType:"json",url:"getchosen.py?"+tags+"season="+seas,mimeType:"text/plain",success:function(data) {
	console.log(data);
	var ret="<tr><th>Selected</th><th>Name</th><th>ID</th><th>Start-Time</th><th>End-Time</th><th>Days</th><th>Season</th></tr>";
	var _id=data["_id"];
	var name=data["name"];
	var start_time=data["start_time"];
	var end_time=data["end_time"];
	var day=data["day"];
	var season=data["seas"];
	for ( var i=0;i<data["_id"].length;i++) {
	    ret+="<tr><td><input type='checkbox' name='"+data["_id"][i]+"' id='"+data["_id"][i]+"' ";
	    if (data["sel"][i]==1) {
		ret+="checked";
	    }
	    ret+="></td>\n";

	    ret+="<td>"+name[i]+"</td>\n";
            ret+="<td>"+_id[i]+"</td>\n";
            ret+="<td>"+start_time[i]+"</td>\n";
            ret+="<td>"+end_time[i]+"</td>\n";
            ret+="<td align='left'>"+day[i]+"</td>\n";
            ret+="<td id='seas"+_id[i]+"'>"+season[i]+"</td></tr>\n";
	}
	console.log(ret);
	//document.getElementById("tablein").innerHTML=ret;
	$("#tablein").html(ret);
	    
    }});
    event.preventDefault();
    
});
//function display() {
 //   var args="";
    
    
    //$.ajax({dataType:"json",url:"getchosen.py?pnum="+optionnum,mimeType:"text/plain",success:function(data) {