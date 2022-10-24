from flask import Flask, request,jsonify,abort
from flask_cors import CORS
from models import setup_db, model_name

def create_app(test_config=None):
    app=Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
        )
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        return response

    @app.route("/",methods=["GET"])
    def hello():
        return "hello world"

    return app