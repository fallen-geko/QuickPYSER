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
    Oh this is the forum script. Notice the async thingy? Thats becuase while testing it,
    I discovered when a new post is uploaded and the page refreshes, the change wont be
    registered immediately. So I put a little delay time to give the post all the time in
    the world (its world) to update.
'''
#import modules for CGI handling
import cgi, cgitb
import theroom
import time
import asyncio
cgitb.enable()
#If this is a room entrance okay save it to our cookiesss
form = cgi.FieldStorage() 
rid = form.getvalue('forRoom')
rpg = form.getvalue('forPage')
#I had to find a way to make the room load pause while waiting for a user to post.
#So i split up the script using asyncio
async def main(wtime):
    dr = theroom.showForum(rid,rpg)
    await asyncio.sleep(wtime)
    if len(dr) < 1:
        dr = '''
        <div class="col-sm-12 col-md-12 col-lg-12"
            style="background-color: #dedef8; box-shadow: inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
             <p>This page is empty!.</p>
        </div>
        '''
    rpage = '''
        <h2>The Lobby</h2>
        <div class="container">
        %s
        </div>
    ''' %dr
    print("Content-Type: text/html\r\n")
    print(rpage)
    
if not theroom.checkCookie():
    print("Content-Type: text/html\r\n")
    print("<h1>Something went wrong</h1>")
else:
    #Is the user making a new post?
    postmsg = form.getvalue('postm')
    waitt = 0
    if postmsg:
        ido = theroom.getIdentification()
        ford = theroom.getForumData(int(rid))
        dt = time.time()
        ford.execute('''INSERT INTO posts (author, content, datetime) VALUES (?,?,?)''',(int(ido[0]),postmsg,dt))
        ford.commit()
        ford.close()
        waitt = 1
        
    asyncio.run(main(waitt))