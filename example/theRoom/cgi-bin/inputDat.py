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
    The little input box thingy that is used to post and stuff. I put it in a separate
    script so when the page updates, it wont. Why not? Well imagine youre writing a long
    message begging for money from a wantok it the page refreshes and you lose it all.
'''
import theroom
import cgi

if not theroom.checkCookie():
    print("Content-Type: text/html\r\n")
    print("<h1>Something went wrong</h1>")
else:  
    print("Content-Type: text/html\r\n")
    print(theroom.inputSamtin())
