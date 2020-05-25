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
    Notes: The CGI script for making a new user. Yes, it just sets up the HTML while the rest of the work
    is done in "theroom.py". I know, its really messy and I keep forgetting to add comments.
'''
#import modules for CGI handling
import cgi, cgitb
from os import environ as enn
import theroom

rpage = '''
    <h2 align="center">Sign Up</h2>
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
        <span style="color: #FF0000;"><a id="errorplace3"></a></span>
        <div class="input-group mb-2">
			<div class="input-group-append">
				<span class="input-group-text"><i class="fas fa-user">Password</i></span>
			</div>
			<input id="inpPWORD2" type="password" name="nmePWORD2" class="form-control input_user" value="" placeholder="password">
		</div>
        <div class="input-group mb-2">
			<div class="input-group-append">
				<span class="input-group-text"><i class="fas fa-user">First Name</i></span>
			</div>
			<input id="inpFNAME" type="text" name="nmeFNAME" class="form-control input_user" value="" placeholder="firstname (optional)">
		</div>
        <div class="input-group mb-2">
			<div class="input-group-append">
				<span class="input-group-text"><i class="fas fa-user">Last Name</i></span>
			</div>
			<input id="inpLNAME" type="text" name="nmeLNAME" class="form-control input_user" value="" placeholder="lastname (optional)">
		</div>
        <div class="input-group mb-2">
			<div class="input-group-append">
				<span class="input-group-text"><i class="fas fa-user">Phone</i></span>
			</div>
			<input id="inpPHONE" type="number" name="nmePHONE" class="form-control input_user" value="" placeholder="phone number (optional)">
		</div>
        <div class="input-group mb-2">
			<div class="input-group-append">
				<span class="input-group-text"><i class="fas fa-user">Email</i></span>
			</div>
			<input id="inpEMAIL" type="email" name="nmeEMAIL" class="form-control input_user" value="" placeholder="email (optional)">
		</div>
        <div class="d-flex justify-content-center mt-3 login_container">
			<button class="btn-primary" type="button" onclick = "
				var un = encodeURI($('#inpUNAME').val());
				var pwa = encodeURI($('#inpPWORD').val());
				var pwb = encodeURI($('#inpPWORD2').val());
				var fn = encodeURI($('#inpFNAME').val());
				var ln = encodeURI($('#inpLNAME').val());
				var pn = encodeURI($('#inpPHONE').val());
				var em = encodeURI($('#inpEMAIL').val());
				signUp(un,pwa,pwb,fn,ln,pn,em);">Submit</button>
		</div>
	</form>
    <hr>
    <div align="center">
    <p><i>Already have an account:</i></p>
    <button align="center" id="signin" type="button" name="nsignin" class="btn-secondary" onclick="changeRoom('portal');">Sign In</button>
    </div>
'''
print("Content-Type: text/html\r\n")
print(rpage)
