import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, ModelName


class WalletTestCase(unittest.TestCase):
    """This class represents the Wallet test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "wallet_test"
        self.database_path = f'postgresql://postgres:postgres@localhost:5432/{self.database_name}'
        print (self.database_path, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_hello(self):
        res = self.client.get("/")
        self.assertEqual(res.data, "hello world")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
