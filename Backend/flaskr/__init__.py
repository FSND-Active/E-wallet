from flask import Flask, request,jsonify,abort
from flask_cors import CORS
from models import *

ITEMS_PER_PAGE = 10


def paginate(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items


def create_app(test_config=None):
    app=Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.route("/",methods=["GET"])
    def hello():
        return "hello world"

    @app.route("/test", methods=["POST"])
    def test():
        body = request.get_json()
        name = body.get("name", None)
        try:
            test = Test(name=name)
            test.insert()
            return jsonify({
                "success": True,
                "test": test
            })
        except:
            abort(422)

    @app.route('/register', methods=['POST'])
    def register_user_or_company():
        body = request.get_json()
        first_name = body.get("firstName", None)
        last_name = body.get("lastName", None)
        company_name = body.get("companyName", None)
        account_type = body.get("accountType", None)
        email = body.get("email", None)
        username = body.get("username", None)
        password = body.get("password", None)
        try:
            if(account_type == "personal"):
                user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                wallet = UserWallet(balance=0)
                details = UserDetail()
                transaction = UserTransaction()
                wallet.transaction.append(transaction)
                user.wallet.append(wallet)
                user.details.append(details)
                user.insert()
                return jsonify({
                    "success": True,
                    "user": user
                })
            else:
                company = Company(company_name=company_name, email=email, username=username, password=password)
                company.insert()
                return jsonify({
                    "success": True,
                    "company": company

                })
        except:
            abort(422)

    @app.route('/users/<int:user_id>/details', methods=['PATCH'])
    def user_details(user_id):
        body = request.get_json()
        gender = body.get("gender", None)
        date_of_birth = body.get("dateOfBirth", None)
        phone_number = body.get("phoneNumber", None)
        occupation = body.get("occupation", None)
        country = body.get("country", None)
        state = body.get("state", None)
        city = body.get("city", None)
        zip_code = body.get("zipCode", None)
        address = body.get("address", None)
        verification_id = body.get("verificationId", None)
        utility_bill = body.get("utilityBill", None)
        try:
            details = UserDetail.query.filter(UserDetail.id==user_id).one_or_none
            if details is None:
                abort(404)
            details["gender"] = gender
            details["date_of_birth"] = date_of_birth
            details["phone_number"] = phone_number
            details["occupation"] = occupation
            details["country"] = country
            details["state"] = state
            details["city"] = city
            details["zip_code"] = zip_code
            details["address"] = address
            details["verification_id"] = verification_id
            details["utility_bill"] = utility_bill
            details.update()
            return jsonify({
                "success": True,
                "company": details
            })
        except:
            abort(422)

    @app.route('/companies/<int:company_id>/details', methods=['PATCH'])
    def company_details(company_id):
        body = request.get_json()
        date_of_registration = body.get("dateOfRegistration", None)
        phone_number = body.get("phoneNumber", None)
        nature_of_business = body.get("natureOfBusiness", None)
        country = body.get("country", None)
        state = body.get("state", None)
        city = body.get("city", None)
        zip_code = body.get("zipCode", None)
        address = body.get("address", None)
        verification_id = body.get("verificationId", None)
        utility_bill = body.get("utilityBill", None)
        try:
            details = CompanyDetail.query.filter(CompanyDetail.id==company_id).one_or_none()
            if details is None:
                abort(404)
            details["date_of_registration"] = date_of_registration
            details["phone_number"] = phone_number
            details["nature_of_business"] = nature_of_business
            details["country"] = country
            details["state"] = state
            details["city"] = city
            details["zip_code"] = zip_code
            details["address"] = address
            details["verification_id"] = verification_id
            details["utility_bill"] = utility_bill
            details.update()
            return jsonify({
                "success": True,
                "company": details
            })
        except:
            abort(422)

    @app.route('/login', methods=['POST'])
    def user_or_company_login():
        body = request.get_json()
        account_type = body.get("accountType", None)
        login = body.get("login", None)
        password = body.get("password", None)
        try:
            if(account_type == "personal"):
                user = User.query.filter(user.email == login).one_or_none()
                if user is None:
                    user = User.query.filter(user.username == login).one_or_none()
                    if user is None:
                        user = User.query.filter(user.wallet.id == login).one_or_none()   
                if user is None:
                    abort(404)
                if user.password == password:
                    return jsonify({
                        "success": True,
                        "user": user
                    })
            else:
                company = Company.query.filter(company.email == login).one_or_none()
                if company is None:
                    company = Company.query.filter(company.username == login).one_or_none()
                    if company is None:
                        company = Company.query.filter(company.wallet.id == login).one_or_none()
                if company is None:
                    abort(404)
                if company.password == password:
                    return jsonify({
                        "success": True,
                        "company": company
                    })
        except:
            abort(422)

    @app.route('/users/<int:user_id>', methods=['PATCH'])
    def user_reset_password(user_id):
        body = request.get_json()
        password = body.get("password", None)
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            user["password"] = password
            if user is None:
                print('user not found')
                abort(400)
            else:
                user.update()
            return jsonify({
                "success": True,
                "user": user
            })
        except:
            abort(422)

    @app.route('/companies/<int:company_id>', methods=['PATCH'])
    def company_reset_password(company_id):
        body = request.get_json()
        password = body.get("password", None)
        try:
            company = Company.query.filter(Company.id == company_id).one_or_none()
            company["password"] = password
            if company is None:
                print('company not found')
                abort(400)
            else:
                company.update()
            return jsonify({
                "success": True,
                "company": company
            })
        except:
            abort(422)

    @app.route('/users', methods=['GET'])
    def get_users():
        try:
            users = User.query.order_by(User.id).all()
            current_users = paginate(request, users)
            if len(current_users) == 0:
                abort(404)
            return jsonify({
                "success": True,
                "users": current_users,
                "totalUsers": len(current_users)
            })
        except:
            abort(422)

    @app.route("/users/<int:user_id>", methods=['GET'])
    def get_user(user_id):
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            if user is None:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "user": user
                }
            )
        except:
            abort(422)

    @app.route('/companies', methods=['GET'])
    def get_companies():
        try:
            companies = Company.query.order_by(Company.id).all()
            current_companies = paginate(request, companies)
            if len(current_companies) == 0:
                abort(404)
            return jsonify({
                "success": True,
                "companies": current_companies,
                "totalcompanies": len(current_companies)
            })
        except:
            abort(422)

    @app.route("/companies/<int:company_id>", methods=['GET'])
    def get_company(company_id):
        try:
            company = Company.query.filter(company.id == company_id).one_or_none()
            if company is None:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "company": company
                }
            )
        except:
            abort(422)

    @app.route('/users/<int:user_id>/wallet', methods=['PATCH'])
    def user_withdraw(user_id):
        body = request.get_json()
        amount = body.get("amount", None)
        try:
            wallet = UserWallet.query.filter(UserWallet.id == user_id).one_or_none()
            if wallet is None:
                print('wallet not found')
                abort(400)
            if wallet["balance"] > amount:
                wallet["balance"] = wallet["balance"] - amount
                wallet.update()
            else:
                abort(400)
            return jsonify({
                "success": True,
                "wallet": wallet
            })
        except:
            abort(422)

    @app.route('/users/<int:user_id>/wallet', methods=['PATCH'])
    def user_deposit(user_id):
        body = request.get_json()
        amount = body.get("amount", None)
        try:
            wallet = UserWallet.query.filter(UserWallet.id == user_id).one_or_none()
            wallet["balance"] = wallet["balance"] + amount
            if wallet is None:
                print('wallet not found')
                abort(400)
            else:
                wallet.update()
            return jsonify({
                "success": True,
                "wallet": wallet
            })
        except:
            abort(422)

    @app.route('/companies/<int:company_id>/wallet', methods=['PATCH'])
    def company_withdraw(company_id):
        body = request.get_json()
        amount = body.get("amount", None)
        try:
            wallet = CompanyWallet.query.filter(CompanyWallet.id == company_id).one_or_none()
            if wallet is None:
                print('wallet not found')
                abort(400)
            if wallet["balance"] > amount:
                wallet["balance"] = wallet["balance"] - amount
                wallet.update()
            else:
                abort(400)
            return jsonify({
                "success": True,
                "wallet": wallet
            })
        except:
            abort(422)

    @app.route('/companies/<int:company_id>/wallet', methods=['PATCH'])
    def company_deposit(company_id):
        body = request.get_json()
        amount = body.get("amount", None)
        try:
            wallet = CompanyWallet.query.filter(CompanyWallet.id == company_id).one_or_none()
            wallet["balance"] = wallet["balance"] + amount
            if wallet is None:
                print('wallet not found')
                abort(400)
            else:
                wallet.update()
            return jsonify({
                "success": True,
                "wallet": wallet
            })
        except:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
                "success": False,
                "error": 400,
                "message": "bad request",
                }), 400)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found",
                }), 404)

    @app.errorhandler(405)
    def not_allowed(error):
        return (jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed",
                }), 405)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable",
                }), 422)

    @app.errorhandler(500)
    def unprocessable(error):
        return (jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error",
                }), 500)

    return app