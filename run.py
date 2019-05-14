from app.server import app
from app.server import db

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)