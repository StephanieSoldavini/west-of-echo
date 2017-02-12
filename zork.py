import os
import errno
import logging
import subprocess
from flask import Flask
from shutil import copyfile
from flask_ask import Ask, statement, question, session, request

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

SESSION_BASE_PATH = "/home/ubuntu/zork_session/"
SYS_SAVE_FILENAME = "/dsave.dat"
USR_SAVE_FILENAME = "/usr_dsave.dat"

LOAD_CMD = "restore \n "
SAVE_CMD = "\n save"

ZORK_BINARY = "/home/ubuntu/zork/zork"


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def call_zork(uid, action):
    s = subprocess.Popen([ZORK_BINARY], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True, cwd=SESSION_BASE_PATH+uid)
    out, err = s.communicate(input=LOAD_CMD + action + SAVE_CMD, timeout=5)
    return '\n'.join( out.split('\n')[5:-2] )[1:]


@ask.launch
def new_game():
    uid = session.user.userId
    make_sure_path_exists(SESSION_BASE_PATH + uid)
    result = "Welcome to West of Echo.  Zork, for Amazon Echo!\n" + call_zork(uid, "look")
    return question(result)


@ask.intent("ActionIntent")
def action(action):
    uid = session.user.userId
    if action.strip().lower() == "save":
        """ cp dsave.dat user_dsave.dat """
        copyfile(SESSION_BASE_PATH + uid + SYS_SAVE_FILENAME, SESSION_BASE_PATH + uid + USR_SAVE_FILENAME)
        result = "Saved."
    elif action.strip().lower() == "restore":
        """ cp user_dsave.dat dsave.dat """
        if (os.path.isfile(SESSION_BASE_PATH + uid + USR_SAVE_FILENAME)):
            copyfile(SESSION_BASE_PATH + uid + USR_SAVE_FILENAME, SESSION_BASE_PATH + uid + SYS_SAVE_FILENAME)
        result = "Restored."
    else:
        result = call_zork(uid, action)
    result = action + "\n . . . \n" + result
    return question(result)

@ask.session_ended
def session_ended():
    if (request.reason == "USER_INITIATED"):
        uid = session.user.userId
        os.remove(SESSION_BASE_PATH + uid + SYS_SAVE_FILENAME)
    return statement("Goodbye.")


#if __name__ == '__main__':
#    app.run(debug=True)
