from flask import Flask, request,jsonify,abort
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime
from auth.auth import AuthError,encode_jwt,requires_auth

from models import *
import sys

def create_app(test_config=None):
    app=Flask(__name__)
    setup_db(app)
    CORS(app)
    bcrypt=Bcrypt(app)

    SALT=os.getenv("SALT")

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
        fname=req.get("first_name")
        lname=req.get("last_name")
        email=req.get("email")
        uname=req.get("username")
        password=req.get("password")
        if None in [fname,lname,email,uname,password]:
            abort(400)
        if(Users.query.filter(Users.email==email).one_or_none() or Users.query.filter(Users.username==uname).one_or_none()):
            return jsonify({
                "success":False,
                "message":"Sorry user already exists",
                "status":403
            }),403
        try:
            pw_hash= bcrypt.generate_password_hash(password+SALT).decode('utf-8')
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
            if(user is None):
                user=Users.query.filter(Users.username==mail_or_uname).one_or_none()
                if(user is not None):
                    if(bcrypt.check_password_hash(user.password,password+SALT)):
                        return jsonify({
                            "success":True,
                            "status":200,
                            "jwt":encode_jwt(user.email,["get:users","post:users"]).decode("ASCII"),
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
            if(bcrypt.check_password_hash(user.password,password+SALT)):
                return jsonify({
                    "success":True,
                    "status":200,
                    "jwt":encode_jwt(user.email,["get:users","post:users"]).decode("ASCII"),
                    "user":user.email,
                    "message":""
                }),200
            else:
                abort(404)
        except:
            abort(400)


    @app.route('/users/pay',methods=['POST'])
    @requires_auth("post:users")
    def pay_user(payload):
        try:
            req= request.get_json()
            to=str(req.get("unam_or_mail"))
            amount=int(req.get('amount'))
            sender=str(payload["email"])
            if (amount==0 or None in [sender,to,amount] or to ==sender):
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
            if (None in [sender_wallet, to_wallet]):
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
            
            return jsonify({
                "success":False,
                "status":422,
                "message":"An error occured"
            }),422


    @app.route("/users/logout",methods=["POST"])
    def user_logout():
        pass


    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "status": 404,
            "success": False,
            "message": "resource not found"
        }),404


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "status":405,
            "message":"Method is not allowed",
            "success":False
        }),405

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


    @app.errorhandler(AuthError)
    def get_auth_error(error):
        return jsonify({
            "success": False,
            "status": error.status_code,
            "message": error.error
        }), error.status_code
    return app


