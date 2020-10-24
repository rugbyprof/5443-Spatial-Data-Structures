from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

import pymongo  # package for working with MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    print(request.args)
    return '<h1>Index Page</h1>'   

@app.route('/country/<string:name>')
def get_country_border(name):
    global db
    countries = db["countries"]

    lines = []
    points = {'lat':[],'lon':[],'latlon':[]}

    for obj in countries.find({"properties.ADMIN" : name}, { "geometry.coordinates": 1, "_id": 0 }):
        lines.append(obj)

    print(lines)
    
    for group in lines[0]['geometry']['coordinates']:
        #print(group)
        for line in group:
            #print(line)
            for point in line:
                points['lat'].append(point[1])
                points['lon'].append(point[0])
                points['latlon'].append(point)

    return jsonify({"points":points,"name":name})

@app.route('/earthquake/<int:id>')
def earthquake(id):
    return '<h1>Earthquakes!</h1>'   

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)
