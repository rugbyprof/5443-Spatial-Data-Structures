
https://flask.palletsprojects.com/en/1.1.x/quickstart/


- Set do debug mode for auto reload browser
```
export FLASK_ENV=development
```

- choose which port to run on
```
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)
```

- dealing with url parameters
https://stackoverflow.com/questions/24892035/how-can-i-get-the-named-parameters-from-a-url-using-flask
```python 
from flask import request

@app.route(...)
def login():
    username = request.args.get('username')
    password = request.args.get('password')
```


https://www.kite.com/python/docs/flask.jsonify


```python
from flask import jsonify

@app.route('/_get_current_user')
def get_current_user():
    return jsonify(username=g.user.username,
                   email=g.user.email,
                   id=g.user.id)
```


https://www.freecodecamp.org/news/here-is-the-most-popular-ways-to-make-an-http-request-in-javascript-954ce8c95aaa/