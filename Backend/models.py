import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv()
database_name = os.getenv('DB_NAME')
database_user = os.getenv('DB_USER')
database_password = os.getenv('DB_PASS',)
database_network = os.getenv('DB_NET', 'localhost:5432')
database_path = 'postgresql://{}:{}@{}/{}'.format(
    database_user, database_password, database_network, database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Users

"""


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    transactions= db.relationship('UserTransactions',backref='users',lazy=True)
    wallet=db.relationship('UserWallet',backref='users',lazy=True,cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username
        }


"""
User Details

"""


class UserDetails(db.Model):
    __tablename__ = "users_details"
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(7), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    occupation = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String, nullable=False)
    verification_id = db.Column(db.String(20), nullable=False)
    utility_bill = db.Column(db.String(50), nullable=False)
    # user = db.Column(db.String,db.ForeignKey('users.email'),nullable=True)

    def __init__(self, gender, date_of_birth, phone_number, occupation, country, state, city, zip_code, address, verification_id, utility_bill):
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.occupation = occupation
        self.country = country
        self.state = state
        self.city = city
        self.zip_code = zip_code
        self.address = address
        self.verification_id = verification_id
        self.utility_bill = utility_bill

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "phone_number": self.phone_number,
            "occupation": self.occupation,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "zip_code": self.zip_code,
            "address": self.address,
            "verification_id": self.verification_id,
            "utility_bill": self.utility_bill
        }


"""
Companies

"""


class Companies(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    transactions= db.relationship('CompanyTransactions',backref='companies',lazy=True)

    def __init__(self, company_name, email, username, password):
        self.company_name = company_name
        self.email = email
        self.username = username
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "company_name": self.company_name,
            "email": self.email,
            "username": self.username
        }


"""
Companies Details

"""


class CompanyDetails(db.Model):
    __tablename__ = "company_details"
    id = db.Column(db.Integer, primary_key=True)
    date_of_registration = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    nature_of_business = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String, nullable=False)
    verification_id = db.Column(db.String(20), nullable=False)
    utility_bill = db.Column(db.String(50), nullable=False)
    # company = db.Column(db.Integer,db.ForeignKey('companies.id'),nullable=True)

    def __init__(self, gender, date_of_registration, nature_of_business, phone_number, country, state, city, zip_code, address, verification_id, utility_bill):
        self.gender = gender
        self.date_of_registration = date_of_registration
        self.phone_number = phone_number
        self.nature_of_business = nature_of_business
        self.country = country
        self.state = state
        self.city = city
        self.zip_code = zip_code
        self.address = address
        self.verification_id = verification_id
        self.utility_bill = utility_bill

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "date_of_registration": self.date_of_registration,
            "phone_number": self.phone_number,
            "nature_of_business": self.nature_of_business,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "zip_code": self.zip_code,
            "address": self.address,
            "verification_id": self.verification_id,
            "utility_bill": self.utility_bill
        }


"""
User Wallet

"""


class UserWallet(db.Model):
    __tablename__ = "user_wallet"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String,db.ForeignKey("users.email"),nullable=False,unique=True)
    

    def __init__(self, balance,user):
        self.balance = balance
        self.user=user

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "balance": self.balance,
            "user":self.user
        }


"""
Company Wallet

"""


class CompanyWallet(db.Model):
    __tablename__ = "company_wallet"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)
    # company = db.Column(db.Integer,db.ForeignKey('companies.id'),nullable=False)


    def __init__(self, balance):
        self.balance = balance

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "balance": self.balance
        }



"""
User Transactions

"""


class UserTransactions(db.Model):
    __tablename__ = "user_transactions"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    user = db.Column(db.String,db.ForeignKey('users.email'),nullable=False)



    def __init__(self, type, description, amount, status, date, time,user):
        self.description = description
        self.type = type
        self.amount = amount
        self.status = status
        self.date = date
        self.time = time
        self.user=user

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "description": self.description,
            "type": self.type,
            "amount": self.amount,
            "status": self.status,
            "date": self.date,
            "time": self.time
        }


"""
Company Transactions

"""


class CompanyTransactions(db.Model):
    __tablename__ = "company_transactions"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    company = db.Column(db.Integer,db.ForeignKey('companies.id'),nullable=False)

    def __init__(self,description, type, amount, status, date, time):
        self.description = description
        self.type = type
        self.amount = amount
        self.status = status
        self.date = date
        self.time = time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "description": self.description,
            "type": self.type,
            "amount": self.amount,
            "status": self.status,
            "date": self.date,
            "time": self.time
        }


class BlacklistToken(db.Model):
    __tablename__="blacklist_token"

    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    token=db.Column(db.String(600),nullable=False,unique=True)
    log_date=db.Column(db.DateTime,nullable=False)

    def __init__(self,token,log_date):
        self.token=token
        self.log_date=log_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return ({
            "token":self.token,
            "log_date":self.log_date
        })
