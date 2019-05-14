from source.server import app
from source.server import db

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)