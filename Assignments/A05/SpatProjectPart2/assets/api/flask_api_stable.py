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

    # response = make_response()
    # response.data = result
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return result

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

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


def load_data(path):
    """ Given a path, load the file and handle it based on its
        extension type. So far I have code for json and csv files.
    """
    _, ftype = os.path.splitext(path)   # get fname (_), and extenstion (ftype)
  
    if os.path.isfile(path):            # is it a real file?
        with open(path) as f:
            
            if ftype == ".json" or ftype == ".geojson":        # handle json
                data = f.read()
                if isJson(data):
                    #print(data)
                    return json.loads(data)
                
            elif ftype == ".csv":       # handle csv with csv reader
                with open(path, newline='') as csvfile:
                    data = csv.DictReader(csvfile)
                
                    return list(data)
    return None

"""
  ____    _  _____  _      ____    _    ____ _  _______ _   _ ____
 |  _ \  / \|_   _|/ \    | __ )  / \  / ___| |/ / ____| \ | |  _ \
 | | | |/ _ \ | | / _ \   |  _ \ / _ \| |   | ' /|  _| |  \| | | | |
 | |_| / ___ \| |/ ___ \  | |_) / ___ \ |___| . \| |___| |\  | |_| |
 |____/_/   \_\_/_/   \_\ |____/_/   \_\____|_|\_\_____|_| \_|____/

Helper classes to act as our data backend.
"""

STATES = load_data("./data/states.json")
STATE_BBOXS = load_data("./data/us_states_bbox.csv")
FLAGS = load_data("./data/country-json/country-by-flag.json")
CITIES = load_data("./data/major_cities.geojson")

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
    # with open("/Users/griffin/Documents/mapboxtoken.txt") as f:
    #     tok = f.read()
    token = {'token':'pk.eyJ1IjoicnVnYnlwcm9mIiwiYSI6ImNpZ3M1aDZwbzAyMnF1c20xcnM4ZGowYWQifQ.s6ghscOu98he230FV1_72w'}

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


@app.route('/geo/direction/')
def get_direction():
    """ Description: Return the direction between two lat/lon points.
        Params: 
            lng1 (float) : point 1 lng
            lat1 (float) : point 1 lat
            lng2 (float) : point 1 lat
            lat2 (float) : point 1 lat

        Example: http://localhost:8080/geo/direction/?lng1=-98.4035194716&lat1=33.934640760&lng2=-98.245591004&lat2=34.0132220288
    """
    lng1 = request.args.get('lng1',None)
    lat1 = request.args.get('lat1',None)
    lng2 = request.args.get('lng2',None)
    lat2 = request.args.get('lat2',None)

    b = bearing((float(lng1),float(lat1)), (float(lng2),float(lat2)))

    return handle_response([{"bearing":b}],{'lat1':lat1,'lng1':lng1,'lat2':lat2,'lng2':lng2})

@app.route('/states', methods=["GET"])
def states():
    """ Description: return a list of US state names
        Params: 
            None
        Example: http://localhost:8080/states?filter=mis
    """
    filter = request.args.get('filter',None)
    
    if filter:
        results = []
        for state in STATES:
            if filter.lower() == state['name'][:len(filter)].lower():
                results.append(state)
    else:
        results = STATES

    return handle_response(results)

@app.route('/cities', methods=["GET"])
def cities():
    """ Description: return a list of US state names
        Params: 
            None
        Example: http://localhost:8080/cities?id="Los Angeles"
    """
    id = request.args.get('id',None)
    
    if id:
        results = []
        for city in CITIES:
            if id.lower() == city['properties']['name'].lower():
                results.append(city)
    else:
        results = CITIES['features']

    return handle_response(results)

@app.route('/country/flag/', methods=["GET"])
def country_flag():
    """ Description: returns a state flag
        Params: 
            None
        Example: http://localhost:8080/country/flag/?name=
    """

    name = request.args.get('name',None)

    # "country": "Afghanistan",
    #         "flag_base64

    for flag in FLAGS:
        if name == flag['country']:
            return flag['flag_base64']
    return jsonify([])


@app.route('/state_bbox/', methods=["GET"])
def state_bbox():
    """ Description: return a bounding box for a us state
        Params: 
            None
        Example: http://localhost:8080/state_bbox/<statename>
    """
    state = request.args.get('state',None)
    
    if not state:
        results = STATE_BBOXS
        return handle_response(results)
    
    state = state.lower()
    
    results = []
    for row in STATE_BBOXS:
        if row['name'].lower() == state or row['abbr'].lower() == state:
            row['xmax'] = float(row['xmax'])
            row['xmin'] = float(row['xmin'])
            row['ymin'] = float(row['ymin'])
            row['ymax'] = float(row['ymax'])
            results = row
            
    return handle_response(results)

@app.route('/upload/', methods=["POST"])
def upload_stuff():
    """ Description: return a bounding box for a us state
        Params: 
            None
        Example: http://localhost:8080/upload/?param=3
    """

    data = request.values.get("data")
    
    if isJson(data):
        data = json.loads(data)

    print(data)

    return handle_response(data)



# def build_actual_response(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
        

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080,debug=True)
      


