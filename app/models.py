from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import backref, relationship
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
    dollars = db.Column(db.Float, nullable=False, default="1000.0")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mutual_fund = db.relationship('Mutual_Funds',backref='portfolios', lazy='dynamic')
    def __repr__(self):
        return '<Portfolios {}>'.format(self.body)


<<<<<<< HEAD
class current_fund_price(db.Model):
    __tablename__ = 'current_fund_price'
    mutual_funds_id= db.Column(db.Integer, db.ForeignKey('mutual_funds.id'),primary_key=True)
    stocks_id=db.Column(db.Integer, db.ForeignKey('stocks.id'),primary_key=True)
    stocks =  db.relationship('Stocks',back_populates='mf_id')
    mf_id =  db.relationship('Mutual_Funds',back_populates='stocks')
=======
# current_fund_price = db.table(
#     'current_fund_price',
#     db.Column('mfid',db.Integer,db.ForeignKey('mutual_funds.id'), primary_key=True),
#     db.Column('sid',db.Integer,db.ForeignKey('stocks.id'), primary_key=True)
# )

>>>>>>> danbranch

class Mutual_Funds(db.Model):
    __tablename__='mutual_funds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    dollars = db.Column(db.Float)
    total_mf_sector = db.Column(db.Float)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'))
<<<<<<< HEAD
    stocks_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    stocks = db.relationship('current_fund_price',back_populates='mf_id')
    # stocks = db.relationship('Stocks',secondary='current_fund_price')
=======
    sid = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    stock_rel = relationship("Stocks",secondary='current_fund_price')
>>>>>>> danbranch
    def __repr__(self):
        return '<Mutual_Funds {}>'.format(self.id)
    # mutual_funds = db.relationship(
    #     'Mutual_Funds',
    #     secondary='current_fund_price',
    #     primaryjoin=(current_fund_price.c.mfid== id),
    #     backref=db.backref('current_fund_price', lazy='dynamic'), 
    #     lazy='dynamic'
    # )
    #sid = db.relationship('stocks',back_populates='mf_id', secondary='current_fund_price')


class current_fund_price(db.Model):
   __tablename__ = 'current_fund_price'
   mf_id = db.Column(db.Integer, db.ForeignKey('mutual_funds.id'),primary_key=True)
   stocks_id = db.Column(db.Integer, db.ForeignKey('stocks.id'),primary_key=True)
   stock = db.relationship('Stocks',backref=backref('current_fund_price',cascade="all,delete-orphan"))
   mfund = db.relationship('Mutual_Funds',backref=backref('current_fund_price',cascade="all,delete-orphan"))
    

class Stocks(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    ticker_symbol = db.Column(db.String(32), index=True, unique=True)
    legal_name = db.Column(db.String(128), index=True, unique=True)
    total_shares = db.Column(db.Float)
    current_price = db.Column(db.Float)
<<<<<<< HEAD
    mf_id = db.relationship('current_fund_price',back_populates='stocks')
    # mutual_funds_id = db.Column(db.Integer, db.ForeignKey('Mutual_Funds.id'))
    # mutual_funds = db.relationship('Mutual_Funds',secondary='current_fund_price',primaryjoin=(current_fund_price.c.stocks_id== id),backref=db.backref('current_fund_price', lazy='dynamic'), lazy='dynamic')
    # stocks_id = db.relationship('Stocks',secondary='current_fund_price',primaryjoin=(current_fund_price.c.stock_id== id),backref=db.backref('current_fund_price', lazy='dynamic'), lazy='dynamic')
    def __repr__(self):
        return '<Stocks {}>'.format(self.id)
=======
    mfid = db.Column(db.Integer, db.ForeignKey('mutual_funds.id'))
    mf_rel = relationship('Mutual_Funds',secondary="current_fund_price")

    def __repr__(self):
        return '<Stocks {}>'.format(self.id)
        
    # mfs = db.relationship('current_fund_price',back_populates='stocks')
    # mf_id = db.relationship('current_fund_price',back_populates='stocks')
    # stocks_id = db.relationship(
    #     'Stocks',
    #     secondary='current_fund_price',
    #     primaryjoin=(current_fund_price.c.sid== id),
    #     backref=db.backref('current_fund_price', lazy='dynamic'), 
    #     lazy='dynamic'
    # )


    #mf_id = db.relationship('mutual_funds',back_populates='sid', secondary='current_fund_price')

>>>>>>> danbranch
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))