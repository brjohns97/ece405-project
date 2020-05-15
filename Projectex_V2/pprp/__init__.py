from flask import Flask
#from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#bcrypt = Bcrypt(app)

from pprp import routes
