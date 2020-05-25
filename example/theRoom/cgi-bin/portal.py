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
    Notes: Hehehe, okay this one is a troublemaker. I keep on forgetting that I named
    it "portal.py" and not "signin.py" and I keep getting FileNotFound errors
    flying into my face. Oh yeah, I could change it but I am too lazy to.
'''
#import modules for CGI handling
import cgi, cgitb
from os import environ as enn
import theroom
cgitb.enable()
rpage = '''
    <h2 align="center">Sign In</h2>
    <a id="randmsg"></a>
    <form>
        <span style="color: #FF0000;"><a id="errorplace1"></a></span>
		<div class="input-group mb-2">
			<div class="input-group-append">
				<span class="input-group-text"><i class="fas fa-user">Username</i></span>
			</div>
			<input id="inpUNAME" type="text" name="nmeUNAME" class="form-control input_user" value="" placeholder="username">
		</div>
        <span style="color: #FF0000;"><a id="errorplace2"></a></span>
		<div class="input-group mb-2">
			<div class="input-group-append">
				<span class="input-group-text"><i class="fas fa-user">Password</i></span>
			</div>
			<input id="inpPWORD" type="password" name="nmePWORD" class="form-control input_user" value="" placeholder="password">
		</div>
        <div class="d-flex justify-content-center mt-3 login_container">
			<button class="btn-primary" type="button" onclick = "
            var un = encodeURI($('#inpUNAME').val());
            var pw = encodeURI($('#inpPWORD').val());
            signIn(un,pw);">Submit</button>
		</div>
	</form>
    <hr>
    <div align="center">
    <p><i>Don't have an account:</i></p>
    <button id="signup" type="button" class="btn-secondary" onclick="changeRoom('signup');">Sign Up</button>
    </div>
'''
form = cgi.FieldStorage() 
ks = form.getvalue('killses')
if ks == "true":
    getid = theroom.getIdentification()
    theroom.logUserOut()
    sesbase = theroom.sessionPointer(mod=0)
    #Remove old session
    sesbase.execute('''DELETE FROM runningSessions WHERE userID=%s'''%getid[0])
    sesbase.commit()
    sesbase.close()
    rpage += '''
    <script language = "javascript" type = "text/javascript">
        userName = "";
        userToken = "";
        passWord = "";
        isLoggedIn = false;
    </script>
    '''
try:
    ku = int(form.getvalue('klusr'))
    if (ku):
        theroom.delUser(ku)
except TypeError:
    pass
print("Content-Type: text/html\r\n")
print(rpage)
