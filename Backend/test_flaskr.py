import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from auth.auth import encode_jwt
from flaskr import create_app
from flask_bcrypt import Bcrypt
from models import *


class WalletTestCase(unittest.TestCase):
    """This class represents the Wallet test case"""
    

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "wallet_test"
        self.database_path = f'postgresql://postgres:postgres@localhost:5432/{self.database_name}'
        setup_db(self.app, self.database_path)
        bcrypt= Bcrypt(self.app);SALT = os.getenv("SALT")

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        if Users.query.filter_by(email="test@email.com").first() is None:
            Users("testuser","testuser","test@email.com","test@email.com",bcrypt.generate_password_hash("test"+SALT).decode("utf-8")).insert()
        
        if Users.query.filter_by(email="test@email.com").first() is None:
            Users("testuser2","testuser2","test2@email.com","test2@email.com",bcrypt.generate_password_hash("test2"+SALT).decode("utf-8")).insert()
        self.testjwt=encode_jwt("test@gmail.com",["get:user","post:user"])
        self.testjwt2=encode_jwt("test@gmail.com",["get:user","post:user"])


    def tearDown(self):
        """Executed after reach test"""
        pass
    

    def test_encode_jwt(self):
        ''' it test jwt is encoded and exists'''
        self.assertTrue(self.testjwt and self.testjwt2)
        self.assertTrue(isinstance(self.testjwt,bytes)and isinstance(self.testjwt2,bytes))


    def test_hello(self):
        res = self.client().get("/")
        self.assertEqual(res.data.decode('UTF-8'), "hello world")

    def test_register_user(self):
        '''Test valid registration'''
        '''it should error if form is empty'''
        res= self.client().post("/users/register")
        data= json.loads(res.data)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"],"Bad Request")
        self.assertEqual(res.status_code,400)

        '''it should fail if user exists'''
        res= self.client().post("/users/register",json={"first_name":"test","last_name":"test",
        "email":"test2@email.com","username":"test2@email.com","password":"test2"})
        data=json.loads(res.data)
        self.assertTrue(res.status_code==403)
        self.assertTrue(data["message"]=="Sorry user already exists")

        '''it should register valid user'''
        res= self.client().post("/users/register",json={"first_name":"test","last_name":"test",
        "email":"test5@email.com","username":"test5","password":"test5"})
        Users.query.filter_by(email="test5@email.com").one_or_none().delete()
        data= json.loads(res.data)
        self.assertTrue(res.status_code==200)
        self.assertEqual(data["email"],"test5@email.com")

    def test_login_user(self):
        '''Test valid login'''
        '''it should fail if does not exist'''
        res=self.client().post("/users/login",json={"uname_or_mail":"test","password":"test"})
        data=json.loads(res.data)
        self.assertFalse(data["success"])
        self.assertTrue(res.status_code==404)
        self.assertEqual(data["message"],"user does not exist")

        '''it should fail if password is wrong'''
        res= self.client().post("/users/login",json={"uname_or_mail":"test@email.com","password":"testfail"})
        data= json.loads(res.data)
        self.assertFalse(data["success"])
        self.assertTrue(res.status_code,403)
        self.assertEqual(data["message"],"unauthorised")

        '''it should login valid user'''
        res= self.client().post("/users/login",json={"uname_or_mail":"test@email.com","password":"test"})
        data= json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertTrue(isinstance(data["jwt"],str))
        self.assertTrue(res.status_code==200)


    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
