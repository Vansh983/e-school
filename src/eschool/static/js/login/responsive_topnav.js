// Phone-responsive topnav function responsive()
function responsive(){
	var topnav=document.getElementById("categories");
	if(topnav.className==="topnav"){
		topnav.className += " responsive";
	} else {
		topnav.className = "topnav";
	}
}