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
    Notes: Once our user succeeds in making a user he comes here. A simple GET check
    is done in case a curious client types in this URL. However, its not gonna stop
    a determined client. 
'''
#import modules for CGI handling
import cgi
import theroom
# Create instance of FieldStorage 
form = cgi.FieldStorage() 
yy = form.getvalue('yes')
# Trys to sign up
pros = theroom.makeRoom(gra,grn,grd)
rpage = ""
if (yy=="yes"):
    rpage = '''
    <h2>New User Made</h2>
    <p class="parago">You may now sign in with your credentials.</p>
	<button align="center" id="signin" type="button" name="nsignin" class="btn-secondary" onclick="changeRoom('portal');">Sign In</button>
    '''
else:
    rpage = '''
    <h2>Are you lost?</h2>
	<p class="parago">Something happened and you came here... Are you supposed to be here?</p>
	<button align="center" id="signin" type="button" name="nsignin" class="btn-secondary" onclick="changeRoom('portal');">Sign In</button>
    '''

print("Content-Type: text/html\r\n")
print(rpage)
