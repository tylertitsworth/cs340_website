from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Mutual_funds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    dollars = db.Column(db.Float)
    total_mf_sector = db.Column(db.Float)

    def __repr__(self):
        return '<Mutual_funds {}>'.format(self.body)

class Stocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker_symbol = db.Column(db.String(32), index=True, unique=True)
    legal_name = db.Column(db.String(128), index=True, unique=True)
    total_shares = db.Column(db.Float)
    current_price = db.Column(db.Float)
    
    def __repr__(self):
        return '<Stocks {}>'.format(self.body)
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))