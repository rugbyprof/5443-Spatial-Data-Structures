from flask import Flask,  url_for
from flask import request
from flask import jsonify
from flask_cors import CORS

import json

app = Flask(__name__)
CORS(app)


"""
   ____        _        
  |  _ \  __ _| |_ __ _ 
  | | | |/ _` | __/ _` |
  | |_| | (_| | || (_| |
  |____/ \__,_|\__\__,_|
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

"""
   ____             _            
  |  _ \ ___  _   _| |_ ___  ___ 
  | |_) / _ \| | | | __/ _ \/ __|
  |  _ < (_) | |_| | ||  __/\__ \
  |_| \_\___/ \__,_|\__\___||___/
"""

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

    response = json.dumps(routes,indent=4)
    response = response.replace("\n","<br>")
    return "<pre>"+response+"</pre>"


@app.route('/book/<string:isbn>', methods=["GET"])
def book(isbn):
    """ book: find a book with isbn.
        Params: isbn (string) : unique id of a book.
        Example: http://localhost/book/1935182080

    """
    global books
    count = 0
    success = True

    data = books.getByIsbn(isbn)

    return handle_response(data)

@app.route('/categories/', methods=["GET"])
def categories():
    """ categories: list all categories.
    """
    global books
    count = 0
    success = True

    data = books.getCategories()

    return handle_response(data)

@app.route('/pages/', methods=["GET"])
def pages():
    """ pages: find books in range of pages.
    """
    global books
    count = 0
    success = True

    start = request.args.get('start',0)
    end  = request.args.get('end',9000)

    filter = ["title","isbn","thumbnailUrl","shortDescription","pageCount"]

    data = books.getByPageCount(start,end,filter)

    return handle_response(data)



"""
  _____      _            _
 |  __ \    (_)          | |
 | |__) | __ ___   ____ _| |_ ___
 |  ___/ '__| \ \ / / _` | __/ _ \
 | |   | |  | |\ V / (_| | ||  __/
 |_|   |_|  |_| \_/ \__,_|\__\___|
"""

def handle_response(data,error=None):
    """ handle_response
    """
    success = True
    count = len(data)
    
    result = {"success":success,"count":count,"results":data}

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


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080,debug=True)
      
