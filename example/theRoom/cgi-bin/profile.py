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
    Notes: This is for viewing and editing your profile (if you have one)
'''
#import modules for CGI handling
import cgi, cgitb
import os
import theroom
cgitb.enable()
if not theroom.checkCookie():
    print("Content-Type: text/html\r\n")
    print("<h1>Something went wrong</h1>")
else:   
    #Get id of user from field storage
    form = cgi.FieldStorage() 
    #Check if there was a user update
    isudate = form.getvalue('uinfc')
    if isudate == "true":
        #Update user info
        #hunt for info using con-win-i-ant function.. hehehe
        todase = theroom.sessionPointer(mod=1)
        c = todase.cursor()        
        moin = theroom.getIdentification()
        eid = moin[0]
        #Okay grab update info from field storage
        fname = form.getvalue('fname')
        lname = form.getvalue('lname')
        phone = form.getvalue('phone')
        email = form.getvalue('email')
        gend = form.getvalue('gend')
        pic = form.getvalue('pic')
        c.execute('''UPDATE enrolled SET firstName = ?, lastName = ?, phoneNum = ?, email = ?, picID = ?, gender = ? WHERE ID=?''',(fname,lname,phone,email,pic,gend,eid))
        todase.commit()
        todase.close()
        
    ks = form.getvalue('usid')
    up = form.getvalue('uppic')
    ido = theroom.getIdentification()
    try:
        cusid = int(ks)
    except TypeError:
        cusid = int(ido[0])
    #hunt for info using con-win-i-ant function.. hehehe
    todase = theroom.sessionPointer(mod=1)
    c = todase.cursor()
    c.execute('''SELECT userName, firstName, lastName, phoneNum, email, picID, gender FROM enrolled WHERE ID=?''',(cusid,))
    alin = c.fetchall()
    todase.close()
    spark = []
    for a in alin[0]:
        spark.append(str(a))
    #Get propic
    picdir = '%s/data/propics/%s.png' % (os.getcwd(),spark[5])
    ppim = 0
    try:
        os.stat(picdir)
        picdir = '../data/propics/%s.png' % spark[5]
        ppim = int(spark[5])
    except FileNotFoundError:
        picdir = '../data/propics/1.png'
        ppim = 0      
    #Translate our gender from codes (None/0 = Rather not say, 1 = Male, 2 = Female, 3 = Other
    try:
        mgen = int(spark[6])
    except (TypeError, ValueError):
        mgen = 0
    if mgen > 3:
        mgen = 0
    mgen = theroom.genTup[mgen]
    rpage = '''
        <script type="text/javascript" language="javascript">
			//To be clear, I used "sex" here as a shortcut for section
			//noken kisi karangi
            var sex = new Array("flip1","flip2");
			function trigger(fid) {
				var lengthOfArray = sex.length;
				for (var i = 0; i < lengthOfArray; i++) {
					if (sex[i] == fid) {
						$("#" + sex[i]).show();
					} else {
						$("#" + sex[i]).hide();
					}
				}
			}
			trigger("flip1");
        </script>
        <h2>'''+spark[0]+'''</h2>
		<div>
			<button type="button" class="btn btn-secondary" onclick="trigger('flip1');">Profile Information</button>
			<hr>
			<div id="flip1" class="container">
				<div class="row">
					<div class="col-md-3 col-sm-3 col-xs-3">
						<img style="width:100%;height:100%;" src="'''+picdir+'''"></img>
					</div>
					<div class="col-md-9 col-sm-9 col-xs-9">
						<div class="row"><strong>First Name:&nbsp;</strong>'''+spark[1]+'''</div>
						<div class="row"><strong>Last Name:&nbsp;</strong>'''+spark[2]+'''</div>
						<div class="row"><strong>Gender:&nbsp;</strong>'''+mgen+'''</div>
						<div class="row"><strong>Phone:&nbsp;</strong>'''+spark[3]+'''</div>
						<div class="row"><strong>Email:&nbsp;</strong>'''+spark[4]+'''</div>
					</div>
				</div>
			</div>
		</div>
    '''
    #Add edit stuff if this is really your profile.. hehehe
    if int(ido[0]) == cusid:
        #Generates the gender selection thingy 
        gendersel = ''
        for i in range(len(theroom.genTup)):
            cgen = ""
            if mgen == theroom.genTup[i]:
                cgen = "selected"
            gendersel += '<option value="%s" %s>%s</option>'%(i,cgen,theroom.genTup[i])
        #Generates the picture selection thingy
        imgsel = ''
        for i in range(len(theroom.imgTup)):
            cimg = ""
            if ppim == i:
                cimg = "selected"
            imgsel += '<option value="%s" %s>%s</option>'%(i,cimg,theroom.imgTup[i])
        rpage += '''
			<div>
				<button type="button" class="btn btn-secondary" onclick="trigger('flip2');">Edit Profile Information</button>
				<hr>
				<div id="flip2" class="container">
					<form>
						<div class="input-group mb-2">
							<div class="input-group-append">
								<span class="input-group-text"><i class="fas fa-user">First Name</i></span>
							</div>
							<input id="inpFNAME" type="text" name="nmeFNAME" class="form-control input_user" value="'''+spark[1]+'''" placeholder="firstname (optional)">
						</div>
						<div class="input-group mb-2">
							<div class="input-group-append">
								<span class="input-group-text"><i class="fas fa-user">Last Name</i></span>
							</div>
							<input id="inpLNAME" type="text" name="nmeLNAME" class="form-control input_user" value="'''+spark[2]+'''" placeholder="lastname (optional)">
						</div>
						<div class="input-group mb-2">
							<div class="input-group-append">
								<span class="input-group-text"><i class="fas fa-user">Phone</i></span>
							</div>
							<input id="inpPHONE" type="number" name="nmePHONE" class="form-control input_user" value="'''+spark[3]+'''" placeholder="phone number (optional)">
						</div>
						<div class="input-group mb-2">
							<div class="input-group-append">
								<span class="input-group-text"><i class="fas fa-user">Email</i></span>
							</div>
							<input id="inpEMAIL" type="email" name="nmeEMAIL" class="form-control input_user" value="'''+spark[4]+'''" placeholder="email (optional)">
						</div>
						<div class="input-group mb-2">
							<div class="input-group-append">
								<span class="input-group-text"><i class="fas fa-user">Gender</i></span>
							</div>
							<select id="GEND" name="npgen" class="form-control input_user">
								'''+gendersel+'''
							</select>
						</div>
						<div class="input-group mb-2">
							<div class="input-group-append">
								<span class="input-group-text"><i class="fas fa-user">Profile Picture</i></span>
							</div>
							<select id="PPIC" name="nppic" class="form-control input_user">
								'''+imgsel+'''
							</select>
						</div>
						<div class="d-flex justify-content-center mt-3 login_container">
							<button class="btn-primary" type="button" onclick = "
							var fn = encodeURI($('#inpFNAME').val());
							var ln = encodeURI($('#inpLNAME').val());
							var pn = encodeURI($('#inpPHONE').val());
							var em = encodeURI($('#inpEMAIL').val());
							var gen = encodeURI($('#GEND').val());
							var pp = encodeURI($('#PPIC').val());
                            updateInfo(fn,ln,pn,em,gen,pp);">Submit</button>
						</div>
					</form>
				</div>
                <button class='btn btn-primary' onclick='
                    delUser(%s);'>Delete Account</button>
			</div>
        ''' % ido[0]
    print("Content-Type: text/html\r\n")
    print(rpage)