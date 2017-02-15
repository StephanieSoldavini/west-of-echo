# west-of-echo
Zork I on the Amazon Echo

Uses an AWS EC2 instance running Ubuntu running apache2 as a reverse proxy to gunicorn to flask to our app.

Zork install:
- Clone frotz: https://github.com/DavidGriffith/frotz
- make dumb
- Download Zork I: https://www.infocom-if.org/downloads/downloads.html

Uses flask-ask:
- https://github.com/johnwheeler/flask-ask.git

Make sure to set config variables in zork.py to point to the correct dfrotz and zork location