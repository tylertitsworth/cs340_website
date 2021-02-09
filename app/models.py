from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    portfolios = db.relationship('Portfolios', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)



class Portfolios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    dollars = db.Column(db.Float, nullable=False, default="1000.0")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mutual_funds = db.relationship('Mutual_Funds',backref='portfolios', lazy='dynamic')

    def __repr__(self):
        return '<Portfolios {}>'.format(self.body)

class Mutual_Funds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    dollars = db.Column(db.Float)
    total_mf_sector = db.Column(db.Float)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'))
    stocks = db.relationship('Stocks',backref='current_fund_price', lazy = 'dynamic')
    def __repr__(self):
        return '<Mutual_Funds {}>'.format(self.id)

class current_fund_price(db.Model):
    __tablename__ = 'current_fund_price'
    mutual_funds_id = db.Column(db.Integer, db.ForeignKey('mutual_funds.id'),primary_key=True)
    stocks_id = db.Column(db.Integer, db.ForeignKey('stocks.id'),primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(['stocks_id'],['stocks.id']),
    )

    
class Stocks(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    ticker_symbol = db.Column(db.String(32), index=True, unique=True)
    legal_name = db.Column(db.String(128), index=True, unique=True)
    total_shares = db.Column(db.Float)
    current_price = db.Column(db.Float)

    mutual_funds = db.relationship('Mutual_Funds',backref='current_fund_price',lazy='dynamic')
    
    def __repr__(self):
        return '<Stocks {}>'.format(self.id)
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))