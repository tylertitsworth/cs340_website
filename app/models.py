from sqlalchemy import ForeignKey,UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.relationships import foreign 
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
    __tablename__='portfolios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    # Check initial_dollars - dollars_invested >= 0 
    initial_investment_amt = db.Column(db.Float, nullable=False, default="1000.0")
    dollars_available = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # mutual_fund = db.relationship('Mutual_Funds',backref='portfolios', lazy='dynamic')
    mf_port_rel = db.relationship("Mutual_Funds", secondary = 'holdings')
    
    def __repr__(self):
        return '<Portfolios {}>'.format(self.id)



class Holdings(db.Model):
    __tablename__='holdings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    port_id_hold = db.Column(db.Integer, db.ForeignKey('portfolios.id'),primary_key=True)
    mf_id_hold = db.Column(db.Integer, db.ForeignKey('mutual_funds.id'),primary_key=True)
    # number of shares for this transaction
    mf_shares = db.Column(db.Float, nullable=True)
    # nav at the transaction
    mf_nav = db.Column(db.Float, nullable=True)

    port_amount_invested = db.Column(db.Float, nullable=False)
    mfund_hold_rel =  db.relationship('Mutual_Funds',backref=backref('Holdings',cascade="all,delete-orphan"))
    port_hold_rel = db.relationship('Portfolios',backref=backref('Holdings',cascade="all,delete-orphan"))
    def __repr__(self):
        return '<Holdings {}>'.format(self.id)




class Mutual_Funds(db.Model):
    __tablename__='mutual_funds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    initial_investment_amt = db.Column(db.Float, nullable=False)
    # Net Asset Value(nav) == nav = dollars_available  + sumproduct (stocks shares * stock shares price) 
    nav = db.Column(db.Float, nullable=True)
    shares_outstanding = db.Column(db.Float, nullable=True)
    dollars_available = db.Column(db.Float, nullable=True)
    dollars_invested = db.Column(db.Float, nullable=True)
    
    total_mf_sector = db.Column(db.Float, nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'))
    sids = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    port_rel = db.relationship("Portfolios", foreign_keys = [portfolio_id])
    stock_rel = db.relationship("Stocks",secondary='current_fund_price')   
    def __repr__(self):
        return '<Mutual_Funds {}>'.format(self.id)
   


class current_fund_price(db.Model):
   __tablename__ = 'current_fund_price'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   mf_id = db.Column(db.Integer, db.ForeignKey('mutual_funds.id'),primary_key=True)
   stocks_id = db.Column(db.Integer, db.ForeignKey('stocks.id'),primary_key=True)
   # the transcaction value of num_shares and price_per_share is the total
   #  transaction amt and would reduce the dollars available with the  associatied with the mfid
   # upgrade the stocks total shares avaible - cfp.num_shares
   total_shares = db.Column(db.Float)
   # at time of transaction
   price_per_share = db.Column(db.Float)
   stock = db.relationship('Stocks',backref=backref('current_fund_price',cascade="all,delete-orphan"))
   mfund = db.relationship('Mutual_Funds',backref=backref('current_fund_price',cascade="all,delete-orphan"))
   def __repr__(self):
        return '<current_fund_price {}>'.format(self.id)

class Stocks(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    ticker_symbol = db.Column(db.String(32), index=True, unique=True)
    legal_name = db.Column(db.String(128), index=True, unique=True)
    current_share_price = db.Column(db.Float, nullable=True)
    total_number_shares = db.Column(db.Float)
    shares_avail =  db.Column(db.Float)
    initial_offering_price = db.Column(db.Float)
    sector_id = db.Column(db.Integer, db.ForeignKey('sectors.id'))
    mf_rel = db.relationship('Mutual_Funds',secondary="current_fund_price")
    
    def __repr__(self):
        return '<Stocks {}>'.format(self.id)
        
class Sectors(db.Model):
    __tablename__ = 'sectors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    stock_sector_rel = db.relationship('Stocks',backref='portfolios', lazy='dynamic')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))