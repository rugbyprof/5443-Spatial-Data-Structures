from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

import json

app = Flask(__name__)
CORS(app)


class BooksData():
    def __init__(self):
        with open('books.json','r') as f:
            data = f.read()

        self.books_dict = json.loads(data)

    def getByIsbn(self,isbn=None):
        for book in self.books_dict:
            if book['isbn'] == isbn:
                return book['isbn']

        return None


books = BooksData()

@app.route('/')
def index():
    print(request.args)
    return '<h1>Answer From A Route</h1>'

@app.route('/book/<string:isbn>')
def book(isbn):
    global books

    return jsonify({"success":True,"count":0,"isbn":isbn})



if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)
