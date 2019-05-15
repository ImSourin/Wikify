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

@app.route('/api/v1',methods=["PUT"])
def update():
    try:
        check = ast.literal_eval(json.dumps(request.get_json()))
    except:
        return make_response("Error in request body", 400)
    else:
        data = request.get_json()
        try:
            query_result = wikitable.query.filter_by(name=data['name']).first()
            if not query_result:
                raise Exception('Entry not found')
        except:
            return make_response("Entry not found", 404)
        else:
            try:
                if data['name']:
                    query_result.name = data['name']
                present_params = json.loads(query_result.params)
                if len(data['add'])>0:
                    for param in data['add']:
                        if param not in present_params:
                            present_params.append(param)
                if len(data['remove'])>0:
                    count = 0
                    for param in data['remove']:
                        if param in present_params:
                            present_params.remove(param)
                            count = count + 1
                    if count != len(data['remove']):
                        raise Exception('Request for removing a parameter not present')
                query_result.params = json.dumps(present_params)
            except:
                return make_response("Error in transaction.\nPossible cause : Request for removing a parameter not present", 404)
            else:
                db.session().commit()
                return make_response("Transaction successful", 200)