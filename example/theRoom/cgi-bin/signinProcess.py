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
    Notes: This is just the sign in (or log in) script. Grabs the password an username from the forms,
    runs em through the the log in function and then sends a script to be executed depending on the result.
'''
#import modules for CGI handling
import cgi
import theroom
# Create instance of FieldStorage 
form = cgi.FieldStorage() 
gun = form.getvalue('uname')
gpw = form.getvalue('pword')
# Trys to sign up
pros = theroom.logIn(gun,gpw)
rpage = ""
if (pros[0] == True):
    rpage = '''
        isLoggedIn = true;     
        setTimeout("changeRoom('lobby');",10);
    ''' #% (gun,gpw,pros[1])
    #print(pros[2].output())
else:
    rpage = '''
        var erp1 = document.getElementById('errorplace1');
		var erp2 = document.getElementById('errorplace2');
        erp1.innerHTML="Username or Password is incorrect";
		erp2.innerHTML="Password or Username is incorrect";
    '''

print("Content-Type: text/xml\r\n")
print(rpage)
