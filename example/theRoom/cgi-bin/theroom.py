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
    Notes: The main processing file. Most of the functions that are called in the CGI's are defined right here.
'''
from hashlib import blake2b
from hmac import compare_digest
import sqlite3
import cgi, cgitb
from pathlib import Path
from os import environ as enn
import os
import json
import shutil
import time
import random
import datetime
from http import cookies
cgitb.enable()
oriDir = os.getcwd()
#Gender tuple for profile edits
genTup = ("Rather not say","Male","Female","Other")
#Profile images tuple for profile edits
imgTup = ('None','Apple','Orange','Pineapple','Watermelon')
def sign(cookie):
    SECRET_KEY = b'pseudorandomly generated server secret key'
    AUTH_SIZE = 16
    h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    h.update(cookie)
    return h.hexdigest().encode('utf-8')

def verify(cookie, sig):
    good_sig = sign(cookie)
    return compare_digest(good_sig, sig)

def sessionPointer(mod=0,dnam=oriDir+'/data/sessions.db',dcom='''CREATE TABLE runningSessions(token TEXT PRIMARY KEY, userID INTEGER)'''):
    if mod == 1:
        dnam = oriDir+'/data/users.db'
        dcom='''CREATE TABLE enrolled(ID INTEGER PRIMARY KEY AUTOINCREMENT, userName TEXT NOT NULL, userPass TEXT NOT NULL, access INT NOT NULL,firstName VARCHAR(255), lastName VARCHAR(255), phoneNum INTEGER, email VARCHAR(255), CRTime INTEGER, picID INTEGER, gender INTEGER)'''
    elif mod == 2:
        dnam = oriDir+'/data/rooms.db'
        dcom='''CREATE TABLE rooms(ID INTEGER PRIMARY KEY AUTOINCREMENT, roomAdmin INTEGER,roomName VARCHAR(255) NOT NULL, roomDesc VARCHAR(255) NOT NULL, roomCDate INTEGER NOT NULL)'''
    
    filee = Path(dnam).exists()
    conn = sqlite3.connect(dnam)
    c = conn.cursor()
    if filee == False:
        c.execute(dcom)
    return conn
    
def checkID(uid,pr):
    for ss in pr:
        if uid == ss[0]:
            return True
    return False
    
def delUser(uid):
    getid = getIdentification()
    if int(getid[0]) == int(uid):
        #Kill current session
        sesbase = sessionPointer(mod=0)
        sesbase.execute('''DELETE FROM runningSessions WHERE userID=?''',(getid[0],))
        sesbase.close()
        #Destroy owned rooms
        #Get room database using convienience function
        spo = sessionPointer(mod=2)
        c = spo.cursor()
        c.execute('''SELECT ID FROM rooms WHERE roomAdmin=?''',(getid[0],))
        rms = c.fetchall()
        spo.close()
        for i in rms:
            delRoom(i[0])
        #Delete user files
        try:
            shutil.rmtree('data/users/%s'%getid[0])
        except FileNotFoundError:
            pass
        #Delete user from database
        spo = sessionPointer(mod=1)
        spo.execute('''DELETE FROM enrolled WHERE ID=?''',(getid[0],))
        spo.commit()
        spo.close()
    
def makeUser(username,password,acl=0,fname="",lname="",phone=None,email=""):
    #Load database with convienience function
    spo = sessionPointer(mod=1)
    #Check if username exists
    c = spo.cursor()
    chcur = c.execute('''SELECT userName FROM enrolled WHERE userName = ?''',(username,))
    for uu in chcur.fetchall():
        if uu[0] == username:
            return False
    cur = spo.cursor()
    #Creation time
    ctime = int(time.time())
    #Okay, tupleish this stuffy wuffy
    toin = (username, password, acl, fname, lname, phone, email, ctime)
    #Readys the execution command
    tex = "INSERT INTO enrolled (userName,userPass,access,firstName,lastName,phoneNum,email,CRTime) VALUES (?,?,?,?,?,?,?,?)"
    cur.execute(tex,toin)
    #Create user dir in data if it doesnt exists
    createDir("data/users")
    #Makes the users own directory
    usdir = "data/users/%s" % cur.lastrowid
    createDir(usdir)
    spo.commit()
    spo.close()
    #Makes user database and create tables for later use
    uconn = sqlite3.connect(usdir + "/user.db")
    uconn.execute('''CREATE TABLE messageInbox(ID INTEGER PRIMARY KEY AUTOINCREMENT, fromID INT, content TEXT, datetime INTEGER)''')
    uconn.execute('''CREATE TABLE messageSent(ID INTEGER PRIMARY KEY AUTOINCREMENT, toID INT, content TEXT, datetime INTEGER)''')
    uconn.commit()
    uconn.close()
    return True
    
def makeRoom(roomAdmin, roomName, roomDesc):
    #Get user ID 
    getid = getIdentification()
    if not getid[0]:
        return False
    userID = int(getid[0])
    #Get room database using convienience function
    spo = sessionPointer(mod=2)
    #Get and store current date and time
    ctime = int(time.time())
    #Put data in a tuple
    roomy = (userID, roomName, roomDesc, ctime)
    exs = '''INSERT INTO rooms (roomAdmin, roomName, roomDesc, roomCDate) VALUES (?,?,?,?)'''
    nc = spo.cursor()
    nc.execute(exs,roomy)
    #Get id for room creation and stuff
    rid = nc.lastrowid
    #commit changes and close database
    spo.commit()
    spo.close()
    #create room dir in data if it doesnt exist
    createDir("data/rooms")
    #creates room folder
    rf = "data/rooms/%s" % rid
    createDir(rf)
    #creates room database and tables
    uconn = sqlite3.connect(rf + "/room.db")
    uconn.execute('''CREATE TABLE posts(ID INTEGER PRIMARY KEY AUTOINCREMENT, author INT, content TEXT, datetime VARCHAR(255))''')
    #uconn.execute('''CREATE TABLE messageSent(ID INTEGER PRIMARY KEY AUTOINCREMENT, toID INT, content TEXT, datetime VARCHAR(255))''')
    uconn.commit()
    uconn.close()
    return True
    
def delRoom(rmid):
    getid = getIdentification()
    #Get room database using convienience function
    spo = sessionPointer(mod=2)
    c = spo.cursor()
    #Select all rooms
    rooms=c.execute('''SELECT ID, roomAdmin FROM rooms WHERE ID=?''',(rmid,))
    rmd = c.fetchone()
    if int(getid[0]) == int(rmd[1]):
        try:
            shutil.rmtree('data/rooms/%s'%rmid)
        except FileNotFoundError:
            pass
        spo.execute('''DELETE FROM rooms WHERE ID=?''',(rmid,))
        spo.commit()
    c.close()
    spo.close()
    
def displayRooms():
    getid = getIdentification()
    roomt = ""
    #Get room database using convienience function
    spo = sessionPointer(mod=2)
    #Select all rooms
    rooms=spo.execute('''SELECT ID,roomAdmin, roomName, roomDesc FROM rooms''')
    for room in rooms:
        editQ = ""
        if getid[0] == room[1]:
            editQ='''<button class="btn btn-primary" onclick="
            delRoom(%s)">Delete</button></td></tr>''' % room[0]
        roomt += '''
			<tr><td>%s</td><td>%s</td><td><a href = "#" onclick="changeRoom('lobby');">%s</a></td></tr>
			<tr><td colspan="3">
			<button class="btn btn-md" onclick="
                forumRoom = %s; //Sets the forum room
                forumPage = -1; //Sets the forum page to -1 which defaults to the highest...
                 mainExtra = ''.concat('&forRoom=','%s','&forPage=','-1');
				changeRoom('room');">Enter</button>
                %s
			''' % (room[2],room[3],room[1],room[0],room[0],editQ)
    spo.close()
    if roomt == "":
        roomt = "<i>No rooms created yet. Please make a room!</i>"
    else:
        top = '''<table width="100%">
            <tr><th style="width: 20%">Room Name</th><th style="width: 60%">Room Description</th><th style="width: 20%">Room Owner</th></tr>'''
        roomt = top + roomt + '</table>'
    return roomt
    
def checkToken(tokenA):
    fdat = sessionPointer()
    c = fdat.cursor()
    loaded = c.execute("SELECT * FROM runningSessions")
    fdat.close()
    for colex in loaded:
        if verify(tokenA,colex):
            return True
    return False
    
def randhex():
    rtok1 = int(random.random() * 10000)
    rtok2 = int(random.random() * 1000)
    com = abs(rtok1 - rtok2)
    comlist = [hex(com),hex(rtok1),hex(rtok2)]
    random.shuffle(comlist)
    token = ""
    for a in comlist:
        token += a  
    token = sign(bytes(token,'utf-8'))
    return token
    
def logIn(uUser,uPass):
    todase = sessionPointer(mod=1)
    col = todase.execute('''SELECT * FROM enrolled WHERE userName=?''',(uUser,))
    pasi = 0
    userID = ""
    for cat in col:
        if cat[1]==uUser and cat[2]==uPass:
            pasi = 1
            userID = cat[0]
            break
    todase.close()
    if pasi==1:
        #Okay password and username correct, assign a new session and remove any sessions for the current user ID
        sesbase = sessionPointer(mod=0)
        #Remove old session
        sesbase.execute('''DELETE FROM runningSessions WHERE userID=?''',(userID,))
        #Generate random token
        ntok = randhex()
        #Create new session
        sesbase.execute('''INSERT INTO runningSessions (token, userID) VALUES (?,?)''',(ntok, userID))
        sesbase.commit()
        sesbase.close()
        #COOKIES
        expiration = datetime.datetime.now() + datetime.timedelta(days=30)
        C = cookies.SimpleCookie()
        C["session"] = str(ntok,'utf-8')
        C["session"]["path"] = "/"
        C["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
        print(C) # generate HTTP headers
        return (True, str(ntok,'utf-8'),C)
    else:
        return (False, None)

def logUserOut():
    C = cookies.SimpleCookie()
    C["session"] = ""
    C["session"]["path"] = "/"
    print(C)
    
def listCookies():
    try:
        print(enn['HTTP_COOKIE'])
    except KeyError:
        print('No Cookies!')
        
def createDir(path):
    try:
        os.stat(path)
    except FileNotFoundError:
        os.mkdir(path)
        
def templateLoad(title,body,jsscript=None):
    shown =''
    exjs = "<!-- HIII -->"
    if jsscript != None:
        exjs = '<script type="text/javascript">%s</script>' % jsscript
    
    temp = '''
        <!doctype html><html lang="en"><head><title>The Room - %s</title>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="author" content="Romeo Dabok">
        <meta name="theme-color" content="#FFC97E0">
        <link rel="stylesheet" href="../css/bootstrap.css" type="text/css">
        <link rel="stylesheet" href="../css/room.css" type="text/css">
        <link rel="icon" href="../res/favicnN.ico">
        <script type="text/javascript" src="../js/jquery-3.5.0.js"></script>
        <script type="text/javascript" src="../js/popper.js"></script>
        <script type="text/javascript" src="../js/bootstrap.js"></script>
		<script type="text/javascript">
			var siteDir = "%s";
		</script>
        </head><body><div id="ntor"></div>
        <div id="logger"><div class="row"><div class="offset-md-1 col-md-11 offset-xs-1 col-xs-12">%s</div></div></div>
        <div class="row"><div class="offset-ls-1 col-ls-10 offset-md-1 col-md-10 offset-xs-1 col-xs-10">%s</div></div> 
        <a id="footer"></a>
        %s
        </body></html>''' % (title,"../",shown,body,exjs)
    return temp
    
def getIdentification():
    isCook = checkCookie()
    if (isCook):      
        sesbase = sessionPointer(mod=0)
        #Create new session
        cu = sesbase.cursor()
        tokens = cu.execute('''SELECT userID FROM runningSessions WHERE token=?''',(isCook,))
        retit = False
        for toks in cu.fetchall():
            retit = toks[0]
        sesbase.close()
        if (retit):
            retwal = None
            spo = sessionPointer(mod=1)
            plinky = spo.cursor()
            wal = plinky.execute('''SELECT ID, userName FROM enrolled WHERE ID=?''',(retit,))
            retwal = wal.fetchall()
            spo.close()
            return retwal[0]
    return False
    
def loginTop():
    getid = getIdentification()
    if not getid:
        return ""  
    #This really messy code is the lil navbar
    ret = '''
        <div class="lilpar">
            <table width="100%">
            <tr>
            <td align="left">Logged in as: <span class="dropdown">
                <button type="button" class="btn dropdown-toggle" type="button" id="usr" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"></button>
                <ul class="dropdown-menu" aria-labelledby="usr">
                    <li><button type="button" class="btn" style="max-width:100%;" onclick='
						changeRoom("profile","&usid='''+str(getid[0])+'''");'>See/Edit Profile</button></li>
                    <li><button type="button" class="btn" style="max-width:100%;" onclick='
						changeRoom("createRoom");'>Make Room</button></li>
                    <li><button type="button" class="btn" style="max-width:100%;" onclick='
						changeRoom("portal","&killses=true");'>Sign Out</button></li>
                </ul>
            </span>
			<span>
				<button type="button" class="btn" onclick='
				changeRoom("lobby");'>Lobby</button>
			</span>
            </td>
            </tr>
            </table>
        </div>
        <script language="javascript" type="text/javascript">
            document.getElementById("usr").innerHTML = "'''+getid[1]+'''";
        </script>
    '''
    return ret

def inputSamtin():
    ret = '''
		<hr>
        <div>
            <form>
				<div class="input-group mb-2">
					<div class="input-group-append">
						<span class="input-group-text"><button class="btn btn-primary" type="reset" onclick="
                            var smg = $('#inpMSG').val();
                            if (smg.length > 0) {
                                var enct = encodeURI(smg);
                                forumPost(enct);
                            }
                        ">Send</button></span>
					</div>
					<textarea id="inpMSG" type="text" name="nmeMSG" class="form-control input_user" value="" placeholder="message"></textarea>
				</div>
			</form>
        </div>
    '''
    return ret
    
def checkCookie():
    isCook = None
    try:
        cookie = cookies.SimpleCookie(enn["HTTP_COOKIE"])
        isCook = cookie["session"].value
    except (cookies.CookieError, KeyError):
        return False
    if (isCook):      
        sesbase = sessionPointer(mod=0)
        #Create new session
        cu = sesbase.cursor()
        #Make it a byte like whow it was stored as
        isCook = bytes(isCook,'utf-8')
        tokens = cu.execute('''SELECT token FROM runningSessions WHERE token=?''',(isCook,))
        retit = False
        for toks in cu.fetchall():
            if toks[0] == isCook:
                retit = isCook
        sesbase.commit()
        sesbase.close()
        return retit
    return False 
    
def getForumData(room):
    rf = "data/rooms/%s" % room
    try:
        os.stat(rf+'/room.db')
    except FileNotFoundError:
        return False
    conn = sqlite3.connect(rf + "/room.db")
    return conn
    
def showForum(room,page):#RD117-FREE
    uconn = getForumData(room)
    if not uconn:
        return False
        
    room = int(room)
    page = int(page)
    #If its a negative num okay then we go to the max page
    if (page < 0):
        mp = uconn.cursor()
        mp.execute('''SELECT MAX(ID) FROM posts''')
        ll = mp.fetchone()
        try:
            cal = int(ll[0])
        except TypeError:
            cal = 10
        mp.close()
        while (cal % 10 != 0):
            cal -= 1
        page = int(cal/10)
    #Calculate the posts and page range stuff
    minP = 10 * page 
    maxP = minP + 9
    #Get cursor and displayRooms
    c = uconn.cursor()
    c.execute('''SELECT * FROM posts WHERE ID BETWEEN ? AND ?''',(minP,maxP))
    posts = c.fetchall()
    tdis = ''
    todase = sessionPointer(mod=1)
    #Your id
    getid = getIdentification()
    for ms in posts:
        crid = ms[1]
        fc = todase.cursor()
        fc.execute('''SELECT userName,ID FROM enrolled WHERE ID=?''',(crid,))
        crid = fc.fetchone()
        try:
            fun = crid[0]
            oncl = """onclick='changeRoom("profile","&usid=%s");'""" % str(crid[1])
            if (int(crid[1]) == int(getid[0])):
                fun += " <small>(You)</small>"
        except TypeError:
            fun = "<i>Deleted User</i>"
            oncl = ''
        tst=int(float(ms[3]))
        ptime = datetime.datetime.fromtimestamp(tst)
        tdis += '''
            <div class="row">
                <div class="col-sm-12 col-md-12 col-lg-12"
                    style="background-color: #dedef8; box-shadow: inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
                    <p><button type="button" class="btn" %s>%s</button> <span style="color: #00FF04;">at %s</span></p>
                    <div style="border: 2px inset; margin: 4px; background-color: #FFFFFF;"><p>%s</p></div>
                </div>
            </div>
            ''' % (oncl,fun,ptime,ms[2])
        fc.close()
    todase.close()
    uconn.close()
    #Okay make the page changing interface
    pci = '''
        <div align="center">
			<span>
				<button class="btn btn-sm" onclick="
					forumMaxPage();">&lt;&lt;</button>
				<button class="btn btn-sm" onclick="
					forumNextPage();">&lt;</button>
			</span>
			<span>
				%s
			</span>
			<span>
				<button class="btn btn-sm" onclick="
					forumPrePage();">&gt;</button>
				<button class="btn btn-sm" onclick="
					forumMinPage();">&gt;&gt;</button>
			</span>
        </div>
    ''' % page
    return pci+tdis+pci