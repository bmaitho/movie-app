from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.movies'
app.config['SQLALCHEMY_TACK_MODIFICATIONS']=False

db= SQLAlchemy(app)
migrate =Migrate(app, db)
import models

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)