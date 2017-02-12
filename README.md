# west-of-echo
Zork I on the Amazon Echo

Uses an AWS EC2 instance running Ubuntu running apache2 as a reverse proxy to gunicorn to flask to our app.

Zork install:
- Clone https://github.com/devshane/zork.git 
- Change CFLAGS from -O2 to -g
- Make

Uses flask-ask:
- https://github.com/johnwheeler/flask-ask.git

Make sure to set config variables in zork.py to point to zork binary location

