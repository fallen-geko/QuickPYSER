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

    The ROOM
    Version 0.5b
    By: Romeo Dabok
    Notes: "The ROOM" is intended to demonstrate the usage of QuickPYSER.
    Description: "The ROOM" is a "all Python" project. Yes, its a collection
    of CGI scripts made especially for QuickPYSER. It features a simple log in
    system and a forum for conversing. Oh and it is my attempt to make a single
    page application-ish web service with AJAX.

    "The ROOM" is portable... Very portable. To do so, I used SQLite3 for the
    databases instead of MySQL. So yay! No need to install additional libraries.
    Both QuickPYSER and The Room run with packages included in the Python installation.

    Oh, I used Windows 7 to test this. If you're using another OS - expect the unexpected.
    Also, ROOM is actually an abbreviation for: Romeo's Odd Open Messenger. Used to be
    ROM (Romeo's Open Messenger) but then I got obsessed with Dean Koontz "Odd" series.
    Well ROOM sounds better than ROM anyway.
'''
import configparser as cfp
import subprocess as sps
import sys
import signal
import os
import sqlite3
import pipes
#Saves original directory for future references... just in case it changes
oriDir = os.getcwd()

#Creates config directory if it doesnt exist
try:
    os.stat(oriDir + '\\config')
except FileNotFoundError:
    os.mkdir(oriDir +'\\config')
            
#Load configuration
config = cfp.ConfigParser()
config.read('config\\config.ini')

def loadAndTry(section,key,default):
    ret = ""
    try:
        ret = config[section][key]
    except KeyError:
        ret = default
        try:
            config[section]
        except KeyError:
            config[section] = {}
        config[section][key] = default
        with open('config\\config.ini','w') as f:
            config.write(f)
    return ret

host = loadAndTry('server','host',"")
port = int(loadAndTry('server','port',"8080"))
endall = int(loadAndTry('server','endActExitAll','1'))

serverState = 0
#Just make the pid known... just incase
pid = None
proc = None
##################OKAY THE CONSOLE
print("Welcome to quick serve")
print("")
while True:
    ss = "Start Server"
    if serverState == 1:
        ss = "Stop Server"
    cue = input("Options:\n1: %s\n2: Change Configuration\n3: Quit\n>" % ss)
    cut = cue.strip()
    if cut == "1":
        if serverState == 0:
            # Create serving directory if it doesnt exist
            try:
                os.stat(oriDir + '\\theRoom')
            except FileNotFoundError:
                os.mkdir(oriDir +'\\theRoom')
            #Oh yeah, detach the process.. that way our console will be
            #free to do other stuff while its wantok displays the client requests
            DETACHED_PROCESS = sps.CREATE_NEW_CONSOLE
            proc = sps.Popen([sys.executable,oriDir+"//QuickPYSER.py","-h",str(host),"-p",str(port),"-d",oriDir+'\\theRoom',
                              '-s','yes','-l',oriDir],creationflags=DETACHED_PROCESS)
            #Sets the server state so we will all be aware that the server is already running
            serverState = 1
        elif serverState == 1:
            #Kills the server process and resets the state (if its running)
            try:
                #os.kill(pid,signal.SIGINT)
                proc.kill()
            except OSError:
                pass
            serverState = 0
            #Oh, and clears the sessions if the config says so
            if endall == 1:
                try:
                    os.remove(oriDir+"\\theRoom\\data\\sessions.db")
                except FileNotFoundError:
                    pass
                #Oh yes, when I said "clears", I meant delete the entire database.
                #Bwaahahahahaha
    elif cut == "2":
        while True:
            ocue = input("Options:\n1: Change Host (current: %s)\n2: Change Port (current: %s)\n3: Back\n>" % (host,port))
            ocut = ocue.strip()
            if ocut == "1":
                host = input("Input new host name:\n>")
                config["server"]["host"] = host
            elif ocut == "2":
                npmsg = "Input new port number:\n>"
                while True:
                    nport = input(npmsg)
                    try:
                        port = int(nport)
                        config["server"]["port"] = nport
                        break
                    except ValueError:
                        npmsg = "Please enter an integer value:\n>"
            elif ocut == "3":
                with open('config\\config.ini','w') as f:
                    config.write(f)
                break
    elif cut == "3":
        break
