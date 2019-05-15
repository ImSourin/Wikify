'''Import the app and database object.'''
from source.server import app
from source.server import db

if __name__=="__main__":
    '''Create database(if not already present) and run the app.'''
    db.create_all()
    app.run(debug=True)