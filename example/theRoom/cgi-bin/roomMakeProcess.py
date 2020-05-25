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
    Notes: The CGI script for room making. A js function sets the headers and 
    calls this baby.
'''
#import modules for CGI handling
import cgi, cgitb
from os import environ as enn
import theroom
# Create instance of FieldStorage 
form = cgi.FieldStorage() 
grn = form.getvalue('rname')
grd = form.getvalue('rdes')
gra = form.getvalue('radmin')
# Trys to sign up
pros = theroom.makeRoom(gra,grn,grd)
rpage = ""
if pros == True:
    rpage = '''
        changeRoom('lobby',"&rmsg=newRoom");
    '''
else:
    rpage = '''
        var erp = document.getElementById('roomerr');
        erp.innerHTML = "An error occured while trying to create the room! Please try again.";
    '''

print("Content-Type: text/html\r\n")
print(rpage)
