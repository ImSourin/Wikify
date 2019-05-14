import os
from flask import Flask
from flask import request,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
import json
# from app import app
import ast
import source.helper

db_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/database'
app = Flask(__name__)
database_file = "sqlite:///{}".format(os.path.join(db_dir, "wikify.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# import helper
from source.models import *

@app.route('/api/v1',methods=["POST"])
def insert():
    try:
        check = ast.literal_eval(json.dumps(request.get_json()))
    except:
        return make_response("Error in request body", 400)
    else:
        data = request.get_json()
        wikientry = wikitable(name=data['name'],params=json.dumps(data['params']))
        try:
            query_result = wikitable.query.filter_by(name=data['name']).first()
            if query_result:
                raise Exception("Entry already present")
            db.session().add(wikientry)
        except:
            return make_response("Database constraints not satisfied", 409)
        else:
            db.session().commit()
            return make_response("Entry Inserted", 200)

@app.route('/api/v1',methods=["DELETE"])
def delete():
    try:
        check = ast.literal_eval(json.dumps(request.get_json()))
    except:
        return make_response("Error in request body", 400)
    else:
        data = request.get_json()
        try:
            query_result = wikitable.query.filter_by(name=data['name'])
            if not query_result:
                raise Exception('Entry not found')
        except:
            return make_response("Entry not found", 404)
        else:
            try:
                query_result.delete()
            except:
                return make_response("Error in deletion",403)
            else:
                db.session.commit()
                return make_response("Deletion Successful",200)
