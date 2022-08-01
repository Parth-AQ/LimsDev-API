import json
from flask import Flask, Blueprint
from flask_lambda import FlaskLambda

app = FlaskLambda(__name__)
@app.route('/hello')
def index():
    data = {"message": "Hello, World"}
    print(data)
    return (
        json.dumps(data),
        200,
        {"Content-Type": "application/json"}
    )
