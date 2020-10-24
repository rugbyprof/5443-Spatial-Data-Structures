from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    print(request.args)
    return '<h1>Answer From A Route</h1>'

@app.route('/book')
def book():
    return jsonify({"success":True,"count":0})



if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)
