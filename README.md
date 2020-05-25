# QuickPYSER
QuickPYSER is a helpful script that supposed to simplify the creation of a CGI http server in Python. It is intended for those with limited experience with Python to quickly run a CGI http server. Also, it would be quite useful for those whom want to test CGI scripts on their local machines before uploading it on a server and dont have the time or space (as I type this, my PC only has < 1 Gb or hard disk space remaining so I guess I made this mostly for myself) to download Apache (or some other server software) and reconfigure it. Sadly I didnt come around to making a nice help file for this yet.
## What's inside?
The "QuickPYSER.py" script along with an example project called "TheROOM" that tries to "show-off" what you can do with Python as a CGI.
### The ROOM
The ROOM is an example of a site run on the simple Python http server with Python CGI scripts. It uses AJAX to try make it seem like a application and not a server. Also uses bootstrap to make it look nice no matter what the screen size (sadly my css skills are rusty). Databases are built with SQLite3 - oh yeah, this project is designed to be as portable as possible. 
## Usage
There are actually 3 ways (that I know of) that QuickPYSER 
### Import it as a module
Probably the simplest method. Simply put "QuickPYSER.py" in the same directory as your project and import it with `import QuickPyser`.
### Run it from command-line
Change the working directory to where "QuickPYSER.py" and run it from command-line. Don't forget to pass the -s flag so it starts immediately. Here are some parameters:
```
-d          Serving directory (default = current working directory)
-h          Host (default = "")
-l          Log location (default = current working directory)
-p          Port (default = 8080)
-s          Start serving
```
### Run it as a subprocess
An example of this is provided in the "theRoom.py"

## Supported Operating Systems
While this was tested on Windows 7 and Windows 10, I am quite sure it can run on other operating systems.
## Notes
I wouldnt call myself an expert in Python so please dont be suprised to find inefficient or unorthodox coding methods. Feel free to branch and modify, or clone it, or download it etc.
## Contact
Got questions? You can email me at:
DabokRomeo@protonmail.ch or find me on [Facebook](https://www.facebook.com/RDTUNA)
