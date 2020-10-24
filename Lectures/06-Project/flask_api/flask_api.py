#!/Users/griffin/.pyenv/shims/python
import os
import sys
import json

from flask import Flask,  url_for
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask import send_file

from misc_functions import haversine, bearing

app = Flask(__name__)
CORS(app)


"""
   ____    _  _____  _    
  |  _ \  / \|_   _|/ \   
  | | | |/ _ \ | | / _ \  
  | |_| / ___ \| |/ ___ \ 
  |____/_/   \_\_/_/   \_\
"""

"""
   _   _ _____ ___  ____  
  | | | |  ___/ _ \/ ___| 
  | | | | |_ | | | \___ \ 
  | |_| |  _|| |_| |___) |
   \___/|_|   \___/|____/ 
"""

class UfoData():
    """ UfoData: An example class that provides an interface to a ufo json file.
        Methods:
            getUfos()                   : returns a paginated list of ufo's
            getClosest(lon,lat,radius)  : returns all ufo's within radius of lon,lat
    """
    def __init__(self):
        with open('../../../Data/ufos_export.json') as f:
            data = f.readlines()

        self.ufos = []
        for d in data:
            self.ufos.append(json.loads(d))

        self.page_size = 100
        self.start = 0
        self.stop = self.page_size
    
    def getUfos(self,start=0,stop=100):
        result = self.ufos[start:stop]
        return result

    def getUfoCount(self):
        return [{'ufo_count':len(self.ufos)}]

    def getUfosShapes(self):
        results = []
        for ufo in self.ufos:
            if not ufo['shape'] in results:
                results.append(ufo['shape'])
        return results

    def getUfoNeighbors(self,lng,lat,dist):
        results = []
        
        point1 = (float(lng),float(lat))

        mind = 9999999
        mini = 0

        i = 1
        for ufo in self.ufos:
            if not isFloat(ufo['longitude']) or not isFloat(ufo['latitude']):
                continue
            #print(f"{i} : {ufo['longitude']},{ufo['latitude']}")
            point2 = (float(ufo['longitude']),float(ufo['latitude']))
            hdist = haversine(point1,point2)
            if hdist < mind:
                mini = point2
                mind = hdist
            #print(f"{i} : {hdist} {mini}")
            if hdist <= float(dist):
                results.append(ufo)
            i += 1
        print(f"{mind} {mini}")
        return results
        

    def getUfosByDate(self,start,end):
        i = 0
        results = []
        for ufo in self.ufos:
            date,time = ufo['datetime'].split(' ')
            month,day,year = date.split("/")
            hour,min = time.split(":")

            # print(f"{month}-{day}-{year} {hour}:{min}")

            if int(year) >= int(start) and int(year) <= int(end):
                print(f"{month}-{day}-{year} {hour}:{min}")
                results.append(ufo)

        return results


"""
   ____   ___   ___  _  ______  
  | __ ) / _ \ / _ \| |/ / ___| 
  |  _ \| | | | | | | ' /\___ \ 
  | |_) | |_| | |_| | . \ ___) |
  |____/ \___/ \___/|_|\_\____/ 
"""

class BooksData():
    """ BooksData: An example class that provides an interface to a json library of books.
        Methods:
            getByIsbn(string)       : returns 1 book if found
            getCategories()         : returns all categories
            getByPageCount(int,int) : books between start and end pages
    """
    def __init__(self):
        with open('books.json','r') as f:
            data = f.read()

        self.books_dict = json.loads(data)

    def getByIsbn(self,isbn=None):
        for book in self.books_dict:
            if book['isbn'] == isbn:
                return book

        return None

    def getCategories(self):
        categories = []
        for book in self.books_dict:
            for cat in book['categories']:
                if not cat in categories:
                    categories.append(cat)

        return categories

    def getByPageCount(self,start=0,end=9000,filter=[]):
        results = []
        for book in self.books_dict:
            if book['pageCount'] >= int(start) and book['pageCount'] < int(end):
                if len(filter) == 0:
                    results.append(book)
                else:
                    newbook = {}
                    for k,v in book.items():
                        if k in filter:
                            newbook[k] = v
                    results.append(newbook)
                        
        return results


books = BooksData()
ufos = UfoData()

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
    with open("~/mapboxtoken.txt") as f:
        tok = f.read()
    token = {'token':tok}
    
    return token

@app.route("/", methods=["GET"])
def getRoutes():
    """ getRoutes: this gets all the routes!
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

@app.route('/image/<string:filename>')
def get_image(filename):
    """ Description: Return an image for display
        Params: 
            name (string)  : name of image to return
        Example: http://localhost:8080/image/battle_ship_1.png
    """

    image_dir= "./images/"

    image_path = os.path.join(image_dir,filename)

    if not os.path.isfile(image_path):
        return handle_response([],{'filename':filename,'imagepath':image_path},"Error: file did not exist!")

    return send_file(image_path, mimetype='image/png')

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


"""
   _   _ _____ ___  
  | | | |  ___/ _ \ 
  | | | | |_ | | | |
  | |_| |  _|| |_| |
   \___/|_|   \___/ 
"""

@app.route('/ufo/<int:start>/<int:end>/', methods=["GET"])
def ufo(start,end):
    """ Description: Get all the ufos with pagination
        Params: 
            start (int) : start page count
            end (int)   : end page count
        Example: http://localhost:8080/ufo/100/300/
    """
    global ufos

    data = ufos.getUfos(start,end)

    return handle_response(data,{'start':start,'end':end})

@app.route('/ufo/nearest/', methods=["GET"])
def ufoNearest():
    """ Description: Get all the ufos within some distance
        Params: 
            lng (float)   : longitude
            lat (float)   : latitude
            dist (float)  : distance in miles
        Example: http://localhost:8080/ufo/nearest?lng=34.12345&lat=-124.98787&dist=100
    """
    global ufos

    lng = request.args.get('lng',None)
    lat  = request.args.get('lat',None)
    dist = request.args.get('dist',None)

    if not lng or not lat or not dist:
        return handle_response([],{'lng':lng,'lat':lat,'dist':dist},"Error, you need all the params.")

    data = ufos.getUfoNeighbors(lng,lat,dist)

    return handle_response(data,{'lng':lng,'lat':lat,'dist':dist})


@app.route('/ufo/count/', methods=["GET"])
def ufoCount():
    """ Description: Get count of ufos
        Params: 
            None
        Example: http://localhost:8080/ufo/count/
    """
    global ufos

    data = ufos.getUfoCount()

    return handle_response(data)

@app.route('/ufo/date/<string:start>/<string:end>/', methods=["GET"])
def ufoByDate(start,end):
    """ Description: Get all the ufos with pagination
        Params: 
            start (int) : start year
            end (int)   : end year
        Example: http://localhost:8080/ufo/2007/2008/
    """
    global ufos

    data = ufos.getUfosByDate(start,end)

    return handle_response(data)

@app.route('/ufo/shape/', methods=["GET"])
def ufoShapes():
    """ Description: Get all the different Ufo shapes
        Params: 
            None
        Example: http://localhost:8080/ufo/shape/
    """
    global ufos

    data = ufos.getUfosShapes()

    return handle_response(data)

@app.route('/book/isbn/<string:isbn>', methods=["GET"])
def book(isbn):
    """ Description: find a book with isbn.
        Params: isbn (string) : unique id of a book.
        Example: http://localhost:8080/book/1935182080
    """
    global books

    data = books.getByIsbn(isbn)

    return handle_response(data)

@app.route('/book/categories/', methods=["GET"])
def categories():
    """ Description: get all book categories.
        Params: None
        Example: http://localhost:8080/book/categories/
    """
    global books

    data = books.getCategories()

    return handle_response(data)

@app.route('/book/pages/', methods=["GET"])
def pages():
    """ Description: find books in range of pages between start and end.
        Params: 
            start (int) : start page count
            end (int)   : end page count
        Example: http://localhost:8080/book/pages/
    """
    global books

    start = request.args.get('start',0)
    end  = request.args.get('end',9000)

    filter = ["title","isbn","thumbnailUrl","shortDescription","pageCount"]

    data = books.getByPageCount(start,end,filter)

    return handle_response(data)



"""
   ____  ____  _____     ___  _____ _____ 
  |  _ \|  _ \|_ _\ \   / / \|_   _| ____|
  | |_) | |_) || | \ \ / / _ \ | | |  _|  
  |  __/|  _ < | |  \ V / ___ \| | | |___ 
  |_|   |_| \_\___|  \_/_/   \_\_| |_____|
"""

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
    
    
    return jsonify(result)

def formatHelp(route):
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
    try:
        float(string)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080,debug=True)
      
