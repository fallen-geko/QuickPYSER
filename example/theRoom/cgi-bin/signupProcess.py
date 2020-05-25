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
    Notes: Oh this is just the signup processing stuff. Grabs the form values from the header
    and so on so forth...
'''
import cgi
import theroom
# Create instance of FieldStorage 
form = cgi.FieldStorage() 
# Now populate it with the stuff taken from the form
gun = str(form.getvalue('uname'))
gpw = str(form.getvalue('pword'))
gfn = str(form.getvalue('fname'))
gln = str(form.getvalue('lname'))
gpn = str(form.getvalue('phone'))
gem = str(form.getvalue('email'))
# Trys to sign up
pros = theroom.makeUser(gun,gpw,acl=0,fname=gfn,lname=gln,phone=gpn,email=gem)
if pros == True:
    rpage = '''
        changeRoom('newUser',"&yes=yes");
    ''' 
else:
    rpage = '''
		var erp1 = document.getElementById('errorplace1');
		erp1.innerHTML = "The username %s is already taken. Please use a different one";
    ''' % gun

print("Content-Type: text/xml\r\n")
print(rpage)
