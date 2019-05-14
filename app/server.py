import os
from flask import Flask
from flask import request,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
import json
# from app import app
import ast
import app.helper

db_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/database'
app = Flask(__name__)
database_file = "sqlite:///{}".format(os.path.join(db_dir, "wikify.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# import helper
from app.models import *
