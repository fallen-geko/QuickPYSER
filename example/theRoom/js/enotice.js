function addToString(str,toadd) {
	return str + toadd;
}
function goIn(plc) {
	var rep = "home.py"
	window.location.replace(rep);
}
function insertNavbar() {
	/*var topen = '<div class="navbar" align="center">';
	var tclose = '</div>';
	var tbod = '<div><img id="naLogo" align="center" src="../res/tonlyICN.png"></div><hr><span>';
	tbod = addToString(tbod,'<button type="button" class="btn btn-primary" action="home.py">Home</button>');//<a class="cbuta" href="home.py">Home</a>');
	tbod = addToString(tbod,'<button type="button" class="btn btn-primary">Notices</button>');// | <a class="cbuta" href="hello_get.py">Notices</a>');
	tbod = addToString(tbod,'<button type="button" class="btn btn-primary">Forums</button>');// | <a class="cbuta" href="forumsmain.py">Forums</a>');
	tbod = addToString(tbod,'<button type="button" class="btn btn-primary">Archives</button>');// | <a class="cbuta" href="makecook.py">Archives</a>');
	tbod = addToString(tbod,'<button type="button" class="btn btn-primary">Publisher</button>');// | <a class="cbuta" href="loadlisher.py">Publisher</a>');
	tbod = addToString(tbod,'</span>');*/
	var topen = '<div id="nast" class="row">';
    var tbod = '<div class="col-md-12 col-xs-12"><div class="row">';
	tbod += '<div class="col-md-12 col-xs-12"><h2 align="center">E-Notice</h2></div></a>';
	tbod += '</div><div class="row"><div class="offset-md-1 col-md-10 col-xs-12">';
	tbod += '<button type="button" class="btn btn-md" onclick="goIn(1);">Home</button>';
	tbod += '<button type="button" class="btn btn-md">Notices</button>';
	tbod += '<button type="button" class="btn btn-md">Forums</button>';
	tbod += '<button type="button" class="btn btn-md dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">Profile<span class="caret"></span></button>';
	tbod += '<ul class="dropdown-menu" aria-labelledby="dropdownMenu1"><li><a href="#">Action</a></li><li><a href="#">Another action</a></li><li><a href="#">Something else here</a></li><li role="separator" class="divider"></li><li><a href="#">Separated link</a></li></ul>';
	var tclose = '</div></div></div></div>';
	$('#ntor').replaceWith( topen + tbod + tclose);
	return true;
}
$(document).ready(function() {
	//insertNavbar();
})