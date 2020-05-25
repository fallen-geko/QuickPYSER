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
    Notes: The room creation CGI script. It doesnt do much, just sets the HTML.
    Most of the work is done in "theroom.py"
'''
#import modules for CGI handling
import cgi
import theroom
rpage = '''
    <h2 align="center">Make Room</h2>
    <a id="roomerr"></a>
    <form>
        <span style="color: #FF0000;"><a id="errorplace1"></a></span>
		<div class="input-group mb-2">
			<div class="input-group-append">
				<span class="input-group-text"><i class="fas fa-user">Room Name</i></span>
			</div>
			<input id="inpRNAME" type="text" name="nmeRNAME" class="form-control input_user" value="" placeholder="room name">
		</div>
        <div class="input-group mb-2">
			<div class="input-group-append">
				<span class="input-group-text"><i class="fas fa-user">Description</i></span>
			</div>
			<textarea id="inpRDESC" type="text" name="nmeRDESC" class="form-control input_user" value="" placeholder="room description (optional)"></textarea>
		</div>
        <div class="d-flex justify-content-center mt-3 login_container">
			<button class="btn-primary" type="button" onclick = "makeRoom($('#inpRNAME').val(),$('#inpRDESC').val());">Submit</button>
		</div>
	</form>
'''
print("Content-Type: text/html\r\n")
print(rpage)
