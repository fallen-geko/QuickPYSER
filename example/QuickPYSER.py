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
    QuickPYSER
    Version 0.4
    By Romeo Dabok
    Arguments:
    -d          Serving directory (default = current working directory)
    -h          Host (default = "")
    -l          Log location (default = current working directory)
    -p          Port (default = 8080)
    -s          Start serving
    Note: If you use the default host and port, use localhost:8080 to access
    on your own machine. If you are testing it on a WLAN, use ipconfig (or
    go to your adapter settings) to get your IP Address for testing.
    Also note that this is not intended for production.
'''
import http.server
import socketserver
import socket
import os
import sys
#For logging purposes
from datetime import date

#And here are the defaults!!
DIR = os.getcwd() #-d
CHOST = "" #-h
CPORT = 8080 #-p
START = False #-s
illegalPaths = [] 
logLoc = DIR #-l
count = 0

#And commandline arguments for those who dont do modules.
#Oh maybe there is a better way to do this, but I do not know.
for arg in sys.argv:
    if arg == "-p":
        CPORT = int(sys.argv[count+1])
    elif arg == "-h":
        CHOST = sys.argv[count+1]
    elif arg == "-d":
        DIR = sys.argv[count+1]
    elif arg == "-s":
        START = True
    elif arg == "-l":
        logLoc = sys.argv[count+1]
    count+=1

#This function checks if the path the client is trying to access is allowed
#This feature isnt complete
def isIllegalPath(path):
    for sp in illegalPaths:
        if sp == path:
            return True
    return False

#Override the default class so we can make our own modifications..
class MyCGIHandler(http.server.CGIHTTPRequestHandler):
    #Changes the default messaging logging function to one where itll log it to file
    def log_message(self,format,*args):
        #Get current date for the logname
        cdat = date.today()
        #Okay now use only the month and year so we dont get a new log every day
        nuo = "%s-%s" % (cdat.month,cdat.year)
        #Okay the log location
        logl = logLoc + '\\logs'
        #Now the full log name and dir
        logn = logl+'\\access_%s.log' % nuo
        try:
            os.stat(logl)
        except FileNotFoundError:
            os.mkdir(logl)
            
        try:
            f = open(logn, 'r+')
        except FileNotFoundError:
            f = open(logn, 'w')
        logt = "\n%s - - [%s] %s\n" % (self.address_string(),self.log_date_time_string(),format%args)
        f.seek(0,2)
        f.write(logt)
        f.close()
            
    #Changes the default get functions so itll check whether the client is allowed to access it    
    def do_GET(self):
        cpath = None
        try:
            cpath = self.path
            print(cpath)
        except AttributeError:
            cpath = None
        if cpath==None or isIllegalPath(cpath) == False:
            """Serve a GET request."""
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()
        else:
            self.send_error(403,message="Forbidden",explain="You are not allowed to access this.")
                    
#The function for starting the server
def startServe(host=CHOST,port=CPORT):
    os.chdir(DIR)
    CGIHand = MyCGIHandler
    TCPSer = socketserver.TCPServer
    TCPSer.server_name = host
    TCPSer.server_port = port
    print("Initializing server")
    try:
        with TCPSer((host, port),CGIHand) as httpd:
            print("Server started on port",CPORT)
            httpd.serve_forever()
    except OSError:
        print("Failed to start server.")
        print("The port",port,"may be be currently in use.")
        print("Please try another port")
        input("Press enter to exit")

#Oh if you are using this as a module, you wouldnt really
#Need this.
if START:
    startServe()
