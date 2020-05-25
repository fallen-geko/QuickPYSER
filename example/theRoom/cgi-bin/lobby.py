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
    Notes: The lobby! Oh yeah, you come here after you are logged in..
    Its like the living room of this ROOM (wtf). 
'''
#import modules for CGI handling
import cgi, cgitb
import theroom
cgitb.enable()

if not theroom.checkCookie():
    print("Content-Type: text/html\r\n")
    print("<h1>Something went wrong</h1>")
else:
    #Check if anyone is deleting a room
    form = cgi.FieldStorage() 
    krm = None
    try:
        krm=int(form.getvalue('klroom'))
    except TypeError:
        pass
        
    if (krm):
        theroom.delRoom(krm)
    #Display All rooms
    dr = theroom.displayRooms()
    rmsg = form.getvalue("rmsg")
    if rmsg == "newRoom":
        dr += '''
            <script>
                var rde = document.getElementById("roommsg");
                rde.innerHTML = "<div>New Room Created!</div>";
            </script>
        '''   
    rpage = '''
        <h2>The Lobby</h2>
        <a id="roommsg"></a>
        %s
    ''' % dr
    print("Content-Type: text/html\r\n")
    print(rpage)