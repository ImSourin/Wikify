'''Import the required packages'''
import os
from flask import Flask
from flask import request,make_response
from flask_sqlalchemy import SQLAlchemy
import json
# from app import app
import ast
'''Import the helper functions'''
import source.helper

'''This part sets the path for the database and initializes the flask app which would be used
to run the api. Moreover, it sets the sqlalchemy database uri to point to the actual database.
Finally, it initializes the database object and starts a new database session.'''
db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'database')
app = Flask(__name__)
database_file = "sqlite:///{}".format(os.path.join(db_dir, "wikify.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

'''Import the database model'''
from source.models import *

'''API endpoint for Create operations'''
@app.route('/api/v1',methods=["POST"])
def insert():
    '''This function receives request for inserting a new entry in the database.
    It receives a name and may or may not receive any fields in the form of a json object.
    It creates a new table entry if the database constraints are all satisfied.'''
    try:
        '''check if the json obeject received is valid or not'''
        check = ast.literal_eval(json.dumps(request.get_json()))
    except:
        '''In case of invalid json object return error'''
        return make_response("Error in request body", 400)
    else:
        '''get the json data'''
        data = request.get_json()
        '''create a new table entry with the json data'''
        wikientry = wikitable(name=data['name'],params=json.dumps(data['params']))
        try:
            '''Find if the entry is already present. In such a case, raise an exception.'''
            query_result = wikitable.query.filter_by(name=data['name']).first()
            if query_result:
                '''If an entry with the same name is already present'''
                raise Exception("Entry already present")
            '''In case all fields are valid, add the entry to the database'''
            db.session().add(wikientry)
        except:
            '''In case table entry is already present or any other constraints are not satisfied,
            then the exception thrown is handled here.'''
            return make_response("Database constraints not satisfied", 409)
        else:
            '''Finally if no errors occur, then commit the changes and return message for successful operation.'''
            db.session().commit()
            return make_response("Entry Inserted", 200)

'''API endpoint for Delete oeprations'''
@app.route('/api/v1',methods=["DELETE"])
def delete():
    '''This function receives a name for deleteion from the table. If such a name exists in 
    the table, then the table entry is deleted or else an error is thrown.'''
    try:
        '''check if the json obeject received is valid or not'''
        check = ast.literal_eval(json.dumps(request.get_json()))
    except:
        '''In case of invalid json object return error'''
        return make_response("Error in request body", 400)
    else:
        '''get the json data'''
        data = request.get_json()
        try:
            '''Find if the entry is already present. In not, raise an exception.'''
            query_result = wikitable.query.filter_by(name=data['name'])
            if not query_result:
                raise Exception('Entry not found')
        except:
            '''In case entry is not found in the table, the exception raised is handled here.'''
            return make_response("Entry not found", 404)
        else:
            try:
                '''If entry is found, then delete it.'''
                query_result.delete()
            except:
                '''In case there is any error in deletion, the exception would be handled here.'''
                return make_response("Error in deletion",403)
            else:
                '''Finally if no errors occur, then commit the changes and return message for successful operation.'''
                db.session.commit()
                return make_response("Deletion Successful",200)

'''API endpoint for Update operations'''
@app.route('/api/v1',methods=["PUT"])
def update():
    '''This function receives a request to update a table entry. It receives a json object containing Wadd
    and remove params along with name. The params in add are added to the table entry params and the ones 
    in the remove section removed from the table entry params.'''
    try:
        '''check if the json obeject received is valid or not'''
        check = ast.literal_eval(json.dumps(request.get_json()))
    except:
        '''In case of invalid json object return error'''
        return make_response("Error in request body", 400)
    else:
        '''get the json data'''
        data = request.get_json()
        try:
            '''Find if the entry is already present. In not, raise an exception.'''
            query_result = wikitable.query.filter_by(name=data['name']).first()
            if not query_result:
                raise Exception('Entry not found')
        except:
            '''In case entry is not found in the table, the exception raised is handled here.'''
            return make_response("Entry not found", 404)
        else:
            try:
                '''Get the params already present in the corresponding table entry.'''
                present_params = json.loads(query_result.params)
                '''If there is something to add, then add those params.'''
                if len(data['add'])>0:
                    for param in data['add']:
                        '''To avoid duplicates'''
                        if param not in present_params:
                            present_params.append(param)
                '''If there is something to remove, then remove those params.'''
                if len(data['remove'])>0:
                    for param in data['remove']:
                        if param in present_params:
                            present_params.remove(param)
                        else:
                            '''In case there is a request to remove a parameter that is not initially present
                            or has not been added in the current request, then throw an error.'''
                            raise Exception('Request for removing a parameter not present')
                '''In case there are no errors, update the param column in the table entry.'''
                query_result.params = json.dumps(present_params)
            except:
                '''In case there is an error such as Request for removing a parameter not present, then the exception raised is handled here.'''
                return make_response("Error in transaction.\nPossible cause : Request for removing a parameter not present", 404)
            else:
                '''Finally if no errors occur, then commit the changes and return message for successful operation.'''
                db.session().commit()
                return make_response("Transaction successful", 200)

'''API endpoint for Read oeprations.'''
@app.route('/api/v1',methods=["GET"])
def query():
    '''This function receives a query of the user in the form of a json object containing name and parameter list for 
    which data values are needed. It checks for any error in the request and if not serves the request.'''
    try:
        '''check if the json obeject received is valid or not'''
        check = ast.literal_eval(json.dumps(request.get_json()))
    except:
        '''In case of invalid json object return error'''
        return make_response("Error in request body", 400)
    else:
        '''get the json data'''
        data = request.get_json()
        try:
            '''Find if the entry is already present. In not, raise an exception.'''
            query_result = wikitable.query.filter_by(name=data['name']).first()
            if not query_result:
                raise Exception("No such entry")
            '''Get the parameters listed by the user.'''
            query_params = json.loads(query_result.params)
            '''Get the parameters present in the database.'''
            required_params = data['params']
            try:
                '''If required parameters has a parameter not present in the database,
                then an exception is raised.'''
                if not set(required_params).issubset(set(query_params)):
                    raise Exception("One or more parameters are not present in database")
            except:
                '''Exception raised for Parameters not present in database is handled here.'''
                return make_response("One or more parameters are not present in database",404)
            else:
                '''Construct the url for fetching the initial json object.'''
                url = 'https://en.wikipedia.org/api/rest_v1/page/summary/'+query_result.name
                '''Initialize the final result to be returned as empty.'''
                final_ans = ""
                try:
                    for param in required_params:
                        '''For every parameter requested, get its data item from the json object using the
                        helper function getvalue. In case, the parameter is bad, the helper function returns
                        None and hence an exception is raised.'''
                        value = source.helper.getvalue(param,url)
                        if value is None:
                            raise Exception("Invalid query")
                        '''In case of no errors, final result is updated.'''
                        final_ans = final_ans + str(param) + " : " + str(value) + "\n"
                except:
                    '''In case of invalid paramters exception, error message is thrown.'''
                    return ("Error while fetching.\nPossible Causes : Invalid params.",405)
                else:
                    '''Finally if no errors occur, then commit the changes and return the result for the query.'''
                    return make_response(final_ans,200)
        except:
            '''In case entry is not found in the table, the exception raised is handled here.'''
            return make_response("Entry not found", 404)