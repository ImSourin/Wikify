''' import database object db created in server to define all the tables it would have.'''
from source.server import db
from flask_sqlalchemy import SQLAlchemy

'''model for the database table'''
class wikitable(db.Model):
    __tablename__ = 'wikitable'
    '''name and params are the two columns in the database'''
    name = db.Column(db.Text, primary_key=True)
    params = db.Column(db.Text)
    '''Constructor for wikitable object'''
    def __init__(self,name=None, params=None):
        self.name = name
        self.params = params