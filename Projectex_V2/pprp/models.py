from datetime import datetime
from pprp import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        return ("User('%s', '%s', '%s',)"%(self.username, self.email, self.image_file))
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return ("Post('%s', '%s')"%(self.title, self.date_posted))


class Keg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_drinks = db.Column(db.Integer, nullable=False)
    number_of_hours = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return ("Keg('%d Drinks', '%d Hours')"%(self.number_of_drinks, self.number_of_hours))

