#!/usr/bin/env python
'''
------------------------------------------------------------------------------------------
	Copyright 2020 Romeo Dabok

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
-------------------------------------------------------------------------------------------
    Notes: For the main page. Almost all the main js functions are defined here. This page is split
	into divisions (which will update themselves). Its a really messy script (to humans) and
	I keep forgetting to use comments. Actually, I think I may already forget what some of these
	functions do...
	em nau, inap lo sumuk.
'''
#import modules for CGI handling
import cgi, cgitb
from os import environ as enn
import theroom
cgitb.enable()

decider = "portal"
logged = "false"

if theroom.checkCookie():
    decider = "lobby"
    logged = "true"

home = '''
    //Logged in and stuff
	let userName = "";
	let passWord = "";
	let userToken = "";
	let isLoggedIn = %s;
    let currRoom = "%s";
	let refreshTime = 10000; //10 seconds
	// Okay, forum room and pages here
	let forumRoom = 0;
	let forumPage = 0;

	// Okay this guy is loaded everytime the room changes
	let mainExtra = "";
	// Sets onload to our lil refresh function
	//document.getElementById("output").inner="JQuery Rocks!";
	//window.onload = setupRefresh;
	// Arrays for room stuff... sorry I dont know what else to call em
	const freeRooms = new Array("portal", "signup", "signinProcess", "signupProcess");
	const staticRooms = new Array("portal", "signup", "signinProcess", "signupProcess","roomMakeProcess","lobby","createRoom","profile");
	const datInputRooms = new Array("room","message");
	//AJAX
	var aRequests = new Array();
	if (window.XMLHttpRequest) {
		aRequests.push(new XMLHttpRequest());
		aRequests.push(new XMLHttpRequest());
		aRequests.push(new XMLHttpRequest());
	} else if (window.ActiveXObject) {
		aRequests.push(new ActiveXObject("Microsoft.XMLHttp"));
		aRequests.push(new ActiveXObject("Microsoft.XMLHttp"));
		aRequests.push(new ActiveXObject("Microsoft.XMLHttp"));
	}
	var Request = false;
	if (window.XMLHttpRequest) {
		Request = new XMLHttpRequest();
	} else if (window.ActiveXObject) {
		Request = new ActiveXObject("Microsoft.XMLHTTP");
	}
	// This function checks an array for a value
	function hasItem(array,item) {
		var lengthOfArray = array.length;
		for (var i = 0; i < lengthOfArray; i++) {
			if (item == array[i]) {
				return true;
			}
		}
		return false;
	}
    function setupRefresh()
    {
        setInterval("refreshBlock(0);",refreshTime);
		refreshBlock(1);
    }
	//Sends message 
	function forumPost(post) {
		if (hasItem(datInputRooms,currRoom)) {
			//$('#inputdata').load('inputDat.py?postm='+post+mainExtra);
			changeRoom('room','&postm='+post);
		}
	}
    function refreshBlock(flag,extra)
    {
		if (!extra) {
			extra = "";
		}
		//If there is some extra, make sure they are added nicely
		var stoks = "";
		//Adds main extra
		extra = extra + mainExtra;
		if (extra) {
			stoks = "?";
			var slen = extra.length;
			extra = extra.slice(1,slen);
		}
		//If user is not logged and and is in a room he is not supposed to be in
		//send em to the portal
		if (isLoggedIn == false && (!hasItem(freeRooms,currRoom))) {
			currRoom = "portal";
		}
		//If this is not a static room okay fresh it
		if ((!hasItem(staticRooms,currRoom)) || flag == 1) {
            $('#rooms').load("".concat(currRoom,'.py',stoks,extra));
		}
		//And this is for text input and the lil nav bar
		if (flag == 1 && (!hasItem(freeRooms,currRoom))) {
			$('#lnabar').load('lilnavbar.py');		
			if (hasItem(datInputRooms,currRoom)) {
				$('#inputdata').load('inputDat.py');
			} else {
				$('#inputdata').load('../nullbar.html');
			}
		} else if (flag == 1) {
			$('#lnabar').load('../nullbar.html');
			$('#inputdata').load('../nullbar.html');
		}
    }
	//Change the room
	function changeRoom(room,extra) {
		if (!extra) {
			extra = "";
		}
		currRoom = room;
		refreshBlock(1,extra);
	}
	//Creates new user
	function signUp(uname,pword,pword2,firstname,lastname,phone,email) {
		if (currRoom !== 'signup') {
			return false;
		}
		var error = 0;
		var erp1 = document.getElementById('errorplace1');
		var erp2 = document.getElementById('errorplace2');
		var erp3 = document.getElementById('errorplace3');
		erp1.innerHTML = "";
		erp2.innerHTML = "";
		if (uname == "" || uname.length < 4) {
			erp1.innerHTML="Username field must be at least 4 characters long.";
			error += 1;
		}
		if (pword == "" || pword.length < 5) {
			erp2.innerHTML="Password field must be at least 5 characters long.";
			error += 1;
		}
		if (pword2 !== pword) {
			erp3.innerHTML="Password 2 does not match Password 1";
			error += 1;
		}
		if (error < 1) {
			//If no errors, okay go to the processing room with this long-assed samtin ya
			//changeRoom('signupProcess',"".concat('&uname=',uname,'&pword=',pword,'&fname=',firstname,'&lname=',lastname,'&phone=',phone,'&email=',email));
			if (aRequests[1]) {
				aRequests[1].open("POST","signupProcess.py");
				aRequests[1].setRequestHeader('Content-Type','application/x-www-form-urlencoded');
				aRequests[1].onreadystatechange = function() {
					if (aRequests[1].readyState == 4 && aRequests[1].status == 200) {
						var rt = aRequests[1].responseText;
						console.log(rt);
						setTimeout(rt,5);
					}
				}
				var req = "".concat('uname=',uname,'&pword=',pword,'&fname=',firstname,'&lname=',lastname,'&phone=',phone,'&email=',email);
				aRequests[1].send(req);
			}
		}
	}
	function signIn(uname,pword) {
		if (currRoom !== 'portal') {
			return false;
		}
		var error = 0;
		var erp1 = document.getElementById('errorplace1');
		var erp2 = document.getElementById('errorplace2');
		erp1.innerHTML = "";
		erp2.innerHTML = "";
		if (uname == "" || uname.length < 4) {
			erp1.innerHTML="Username field must be at least 4 characters long.";
			error += 1;
		}
		if (pword == "" || pword.length < 5) {
			erp2.innerHTML="Password field must be at least 5 characters long.";
			error += 1;
		}
		if (error < 1) {
			//TODO: Sign In
			//changeRoom('signinProcess',"".concat('&uname=',uname,'&pword=',pword));
			if(aRequests[0]) {
				aRequests[0].open("POST", 'signinProcess.py');
				aRequests[0].setRequestHeader('Content-Type','application/x-www-form-urlencoded');
				aRequests[0].onreadystatechange = function() {
					if (aRequests[0].readyState == 4 && aRequests[0].status == 200) {
						//Saves the response text in a variable so I do not stain myself
						//typing it with this ruined keyboard of mine.
						var rt = aRequests[0].responseText;
						setTimeout(rt,5);
					}
				}
				aRequests[0].send("uname="+uname+'&pword='+pword);
			}
		}
	}
	function updateInfo(firstname,lastname,phone,email,gend,ppic) {
		changeRoom('profile',"".concat('&uinfc=true&fname=',firstname,'&lname=',lastname,'&phone=',phone,'&email=',email,'&gend=',gend+'&pic=',ppic));
	}
	function makeRoom(rname,rdes) {
		if (currRoom !== 'createRoom') {
			return false;
		}
		var error = 0;
		var erp1 = document.getElementById('errorplace1');
		erp1.innerHTML = "";
		if (rname == "" || rname.length < 4) {
			erp1.innerHTML="Room name must be at least 4 characters long.";
			error += 1;
		}
		if (error < 1) {
			//TODO: Make Room
			//changeRoom('roomMakeProcess',"".concat('&radmin=',userName,'&rname=',encodeURI(rname),'&rdes='+encodeURI(rdes)));
			if (aRequests[2]) {
				aRequests[2].open("POST","roomMakeProcess.py");
				aRequests[2].setRequestHeader('Content-Type','application/x-www-form-urlencoded');
				aRequests[2].onreadystatechange = function() {
					if (aRequests[2].readyState == 4 && aRequests[2].status == 200) {
						var rt = aRequests[2].responseText;
						setTimeout(rt,5);
					}
				}
				aRequests[2].send("".concat('radmin=',encodeURI(userName),'&rname=',encodeURI(rname),'&rdes=',encodeURI(rdes)))
			}
		}
	}
	function changePic(pic) {
		if (currRoom !== 'profile') {
			return false;
		}
		changeRoom('profile',"".concat('&uppic=',pic));
	}
	//For navigating the forum
	function sealHeader() {
		mainExtra = "".concat("&forRoom=",forumRoom,"&forPage=",forumPage);
		changeRoom('room');
	}
	function forumMaxPage() {
		forumPage = -1;
		sealHeader();
	}
	function forumNextPage() {
		forumPage += 1;
		sealHeader();
	}
	function forumPrePage() {
		forumPage -= 1;
		if (forumPage < 0) {
			forumPage = 0;
		}
		sealHeader();
	}
	function forumMinPage() {
		forumPage = 0;
		sealHeader();
	}
	function delRoom(rmid) {
		changeRoom('lobby',"".concat('&klroom=',rmid));
	}
	function delUser(uid) {
		changeRoom('portal',"".concat('&klusr=',uid));
	}
''' % (logged, decider)
total = '''
	<div><h1 align="center">The Room</h1></div>
	<p class="parago">Welcome Romeo's Odd Open Messenger (ROOM).</p>
	<hr>
	<div id = "lnabar"></div>
    <div id = "rooms"></div>
	<div id = "inputdata"></div>
	<div id = "output"></div>
	<script>
	$(document).ready(function() {
		try {
			window.onload=setupRefresh;
		} catch (e){
			//changeRoom = function(room,extra) {
			//}
			rooms.innerHTML = '<h1>This Browser is incompatable with The Room</h1>';
			//window.onload = startInterval;
		}
	});
		
	</script>
'''
rpage = theroom.templateLoad('Home',total,jsscript=home)
print("Content-Type: text/html\r\n")
print(rpage)