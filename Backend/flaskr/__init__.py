from flask import Flask, request,jsonify,abort
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import *
import sys

def create_app(test_config=None):
    app=Flask(__name__)
    setup_db(app)
    CORS(app)
    bcrypt=Bcrypt(app)


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

    @app.route("/users/register",methods=["POST"])
    def register_user():
        req= request.get_json()
        fname=str(req.get("first_name"))
        lname=str(req.get("last_name"))
        email=str(req.get("email"))
        uname=str(req.get("username"))
        password=str(req.get("password"))
        if(fname is None or lname is None or email is None or uname is None or password is None):
            abort(400)
        if(Users.query.filter(Users.email==email)):
            return jsonify({
                "success":False,
                "message":"Sorry user already exists",
                "status":403
            }),403
        try:
            pw_hash= bcrypt.generate_password_hash(password).decode('utf-8')
            Users(first_name=fname,last_name=lname,email=email,username=uname,password=pw_hash)
            Users.insert()
            return jsonify({
                "success":True,
                "status":200,
                "email":email
            })
        except:
            abort(400)

    @app.route("/users/login",methods=["POST"])
    def user_login():
        req= request.get_json()
        mail_or_uname=str(req.get("uname_or_mail"))
        password=str(req.get("password"))
        try:
            user=Users.query.filter(Users.email==mail_or_uname).one_or_none()
            print (user)
            if(user is None):
                user=Users.query.filter(Users.username==mail_or_uname).one_or_none()
                if(user is not None):
                    if(bcrypt.check_password_hash(user.password,password)):
                        return jsonify({
                            "success":True,
                            "status":200,
                            "jwt":223,
                            "user":user.username
                        }),200
                    else:
                        return(jsonify({
                        "success":False,
                        "status":403,
                        "message":"unauthorised"
                    })),403
                else:
                    return(jsonify({
                        "success":False,
                        "status":404,
                        "message":"user does not exist"
                    })),404
            if(bcrypt.check_password_hash(user.password,password)):
                return jsonify({
                    "success":True,
                    "status":200,
                    "jwt":223,
                    "user":user.email
                })
            else:
                abort(404)
        except:
            abort(400)

    @app.route('/user/pay',methods=['POST'])
    def pay_user():
        pass
    return app

