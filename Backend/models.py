from flask_sqlalchemy import SQLAlchemy
import os


database_name = os.getenv('DB_NAME','wallet_test')
database_user= os.getenv('DB_USER','test_user')
database_password= os.getenv('DB_PASS','test_password')
database_network=os.getenv('DB_NET','localhost:5432')
database_path = 'postgresql://{}:{}@{}/{}'.format(database_user,database_password,database_network, database_name)

db= SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Sample model

"""

class model_name(db.Model):
    __tablename__="model_name"

    id = db.Column(db.Integer, primary_key=True)
    args= db.Column(db.String)
    #other topics

    def __init__(self, id, args):
        self.args=args
        self.id=id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format (self):
        return {"id":self.id}
