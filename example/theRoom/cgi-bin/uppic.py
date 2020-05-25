#!/usr/bin/env python
'''
    I forgot why I decided not to use this...
    - Romeo Dabok
'''
#import modules for CGI handling
import cgi, cgitb
import theroom
cgitb.enable()
if not theroom.checkCookie():
    print("Content-Type: text/html\r\n")
    print("<h1>Something went wrong</h1>")
else:   
    #Get id of user from field storage
    form = cgi.FieldStorage() 
    ks = form.getvalue('usid')
    up = form.getvalue('nimg')
    try:
        cusid = int(ks)
    except TypeError:
        ido = theroom.getIdentification()
        cusid = int(ido[0])
        
    #Is the guy uploading a pic?
    if (up):
        print("Content-Type: text/html\r\n")
        print(up)
        if up.file:
            data = item.file.read() # read contents of file
            print cgi.escape(data) # rather dumb action
    #hunt for info using con-win-i-ant function.. hehehe
    srous = input("letssee")