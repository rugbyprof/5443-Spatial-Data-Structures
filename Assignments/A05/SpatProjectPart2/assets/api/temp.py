#!/Users/griffin/.pyenv/shims/python
import os
import sys
import json

from flask import Flask,  url_for
from flask import request
from flask import jsonify
from flask import make_response
from flask_cors import CORS, cross_origin
from flask import send_file
import glob
import csv
from misc_functions import haversine, bearing
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

"""
  _   _ _____ _     ____  _____ ____
 | | | | ____| |   |  _ \| ____|  _ \
 | |_| |  _| | |   | |_) |  _| | |_) |
 |  _  | |___| |___|  __/| |___|  _ <
 |_| |_|_____|_____|_|   |_____|_| \_\

"""

def logg(data):
    with open("logg.log","w") as logger:
        logger.write(json.dumps(data,indent=4))

def handle_response(data,params=None,error=None):
    """ handle_response
    """
    success = True
    if data:
        if not isinstance(data,list):
            data = [data]
        count = len(data)
    else:
        count = 0
        error = "Data variable is empty!"

    
    result = {"success":success,"count":count,"results":data,"params":params}

    if error:
        success = False
        result['error'] = error

    return result

def formatHelp(route):
    """ Gets the __doc__ text from a method and formats it
        for easier viewing. Whats "__doc__"? This text
        that your reading is!!
    """
    help = globals().get(str(route)).__doc__
    if help != None:
        help = help.split("\n")
        clean_help = []
        for i in range(len(help)):
            help[i] = help[i].rstrip()
            if len(help[i]) > 0:
                clean_help.append(help[i])
    else:
        clean_help = "No Help Provided."
    return clean_help

def isFloat(string):
    """ Helper method to test if val can be float
        without throwing an actual error.
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def isJson(data):
    """ Helper method to test if val can be json
        without throwing an actual error.
    """
    try:
        json.loads(data)
        return True
    except ValueError:
        return False





"""
   ____   ___  _   _ _____ _____ ____  
  |  _ \ / _ \| | | |_   _| ____/ ___| 
  | |_) | | | | | | | | | |  _| \___ \ 
  |  _ <| |_| | |_| | | | | |___ ___) |
  |_| \_\\___/ \___/  |_| |_____|____/ 
"""

@app.route("/token", methods=["GET"])
def getToken():
    """ getToken: this gets mapbox token
    """
    with open(".token") as f:
        tok = f.read()
    b64 = base64.b64encode(tok.encode('utf-8'))
    token = {'token':tok,'b64tok':str(b64)}

    return token

@app.route("/", methods=["GET"])
def getRoutes():
    """ getRoutes: this gets all the routes to display as help for developer.
    """
    routes = {}
    for r in app.url_map._rules:
        
        routes[r.rule] = {}
        routes[r.rule]["functionName"] = r.endpoint
        routes[r.rule]["help"] = formatHelp(r.endpoint)
        routes[r.rule]["methods"] = list(r.methods)

    routes.pop("/static/<path:filename>")
    routes.pop("/")

    response = json.dumps(routes,indent=4,sort_keys=True)
    response = response.replace("\n","<br>")
    return "<pre>"+response+"</pre>"








        

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080,debug=True)
      


