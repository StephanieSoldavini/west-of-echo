import logging

from random import randint
from flask import Flask
from flask_ask import Ask, statement, question, session
from pprint import pprint as pp
import os
import errno
import subprocess

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

SESSION_BASE_PATH = "/home/ubuntu/zork_session/"

LOAD_CMD = "restore \n "
SAVE_CMD = "\n save"

ZORK_BINARY = "/home/ubuntu/zork/zork"

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


@ask.launch
def new_game():
    #uid = session.user.userID
    #make_sure_path_exists(SESSION_BASE_PATH + uid)
    s = subprocess.Popen([ZORK_BINARY], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    out, err = s.communicate(input="restore, look", timeout=5)
    #result = list(out.decode("utf-8"))[5:-1]
    result = '\n'.join( out.split('\n')[5:-1] )
    # s.stdout.readline()
    return question("Welcome to Zork!\n\n" + result)


@ask.intent("ActionIntent")
def action(action):
    s = subprocess.Popen([ZORK_BINARY], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    print("##########", LOAD_CMD + action + SAVE_CMD)
    out, err = s.communicate(input=LOAD_CMD + action + SAVE_CMD, timeout=5)
    result = '\n'.join( out.split('\n')[5:-2] )[1:]
    print("#########2", result)
    print("#########3", '\n'.join( out.split('\n')))
    return question(result)


#if __name__ == '__main__':
#    app.run(debug=True)
