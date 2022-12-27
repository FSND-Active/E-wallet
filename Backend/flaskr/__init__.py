from flask import Flask, request,jsonify,abort
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime,timedelta
from functools import wraps

from models import *
import sys
import jwt

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
        print(fname,lname,email,uname,password)
        if(fname is None or lname is None or email is None or uname is None or password is None):
            abort(400)
        if(Users.query.filter(Users.email==email).one_or_none() or Users.query.filter(Users.username==uname).one_or_none()):
            return jsonify({
                "success":False,
                "message":"Sorry user already exists",
                "status":403
            }),403
        try:
            pw_hash= bcrypt.generate_password_hash(password).decode('utf-8')
            print(pw_hash)
            user=Users(first_name=fname,last_name=lname,email=email,username=uname,password=pw_hash)
            print(user)

            
            wallet=UserWallet(balance=int(0),user=email)
            
            wallet.insert()
            user.insert()
            return jsonify({
                "success":True,
                "status":200,
                "email":email,
                "message":""
            }),200
        except:
            db.session.rollback()
            db.session.close()
            print(sys.exc_info())
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
                        payload= {
                            "email":user.email,
                            "permission":["get:user","post:user"],
                            "exp":datetime.utcnow() + timedelta(minutes=60),
                            "iat":datetime.utcnow()
                        }
                        return jsonify({
                            "success":True,
                            "status":200,
                            "jwt":jwt.encode(payload,os.getenv("KEY"),"HS256"),
                            "user":user.username,
                            "message":""
                        }),200
                    else:
                        return jsonify({
                        "success":False,
                        "status":403,
                        "message":"unauthorised"
                    }),403
                else:
                    return jsonify({
                        "success":False,
                        "status":404,
                        "message":"user does not exist"
                    }),404
            if(bcrypt.check_password_hash(user.password,password)):
                payload= {
                    "email":user.email,
                    "permission":["get:user","post:user"],
                    "exp":datetime.utcnow() + timedelta(minutes=60),
                    "iat":datetime.utcnow()
                }
                return jsonify({
                    "success":True,
                    "status":200,
                    "jwt":jwt.encode(payload,os.getenv("KEY"),"HS256"),
                    "user":user.email,
                    "message":""
                }),200
            else:
                abort(404)
        except:
            abort(400)


    #@verify_jwt_auth()
    @app.route('/users/pay',methods=['POST'])
    def pay_user():
        try:
            req= request.get_json()
            to=str(req.get("unam_or_mail"))
            amount=int(req.get('amount'))
            sender=str(req.get('sender'))# will change this to get email from verified jwt
            if (amount==0 or None in [to,amount,sender]):
                return jsonify({
                    "message":"invalid input",
                    "status":403,
                    "success":False
                }),403
        except:
            abort(422)
        
        try:
            sender_wallet=UserWallet.query.filter(UserWallet.user==sender).one_or_none()
            to_wallet=UserWallet.query.filter(UserWallet.user==to).one_or_none()
            if (sender_wallet is None or to_wallet is None):
                return jsonify({
                    "success":False,
                    "status":404,
                    "message":"User wallet not found"
                }),404
            if (sender_wallet.balance<amount):
                return jsonify({
                    "success":False,
                    "status":404,
                    "message":"Insufficient Balance"
                }),404
        
            sender_wallet.balance=sender_wallet.balance-amount
            to_wallet.balance=to_wallet.balance+amount
    
            sender_receipt=UserTransactions(type="Debit",description=to_wallet.user,amount=amount,status=True,
            date=datetime.utcnow().date().isoformat(),time=datetime.utcnow().time().isoformat(),user=sender_wallet.user)

            to_receipt=UserTransactions(type="Credit",description=sender_wallet.user,amount=amount,status=True,
            date=datetime.utcnow().date().isoformat(),time=datetime.utcnow().time().isoformat(),user=to_wallet.user)
            

            sender_wallet.update()
            to_wallet.update()
            sender_receipt.update()
            to_receipt.update()

            return jsonify({
                "success":True,
                "status":200,
                "message":sender_receipt.format()
            }),200
        except:
            db.session.rollback()
            sender_wallet=UserWallet.query.filter(UserWallet.user==sender).one_or_none()
            to_wallet=UserWallet.query.filter(UserWallet.user==to).one_or_none()
            sender_receipt=UserTransactions(type="Debit",description=to_wallet.user,amount=amount,status=False,
            date=datetime.utcnow().date().isoformat(),time=datetime.utcnow().time().isoformat(),user=sender_wallet.user)
            sender_receipt.update()
            print(sys.exc_info())
            
            return jsonify({
                "success":False,
                "status":422,
                "message":"An error occured"
            }),422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "status": 404,
            "success": False,
            "message": "resource not found"
        }),404

    @app.errorhandler(422)
    def cant_process(error):
        return jsonify({
            "status": 422,
            "success": False,
            "message": "Request unprocessable"
        }),422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "status": 400,
            "success": False,
            "message": "Bad Request"
        }),400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "status": 500,
            "success": False,
            "message": "Internal server error"
        }),500
    return app


