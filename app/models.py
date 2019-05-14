from app.server import db
from flask_sqlalchemy import SQLAlchemy

class wikitable(db.Model):
    __tablename__ = 'wikitable'
    name = db.Column(db.Text, primary_key=True)
    params = db.Column(db.Text)

    def __init__(self,name=None, params=None):
        self.name = name
        self.params = params