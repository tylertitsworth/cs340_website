import re
from flask import render_template, flash, redirect, url_for, request
from sqlalchemy.orm import query
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddMutualFundsForm, AddStocksForm
from flask_login import login_required, current_user, login_user, logout_user
from app.models import  User, Mutual_Funds, Stocks
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    # see this variable
    user = {'username': 'example'}
    # variable store for a loop
    posts = [
        {
            'author': {'username': 'example'},
            'body': 'test_text1'
        }
    ]
    # notice the variable inclusions in list form on the render_template() function
    return render_template('index.html', title='Home Page', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)




@app.route('/mutualFunds',methods=['GET', 'POST'])
def mutualFunds():
    results = Mutual_Funds.query.all()
    form = AddMutualFundsForm()
    if form.validate_on_submit():
        mutual_fund = Mutual_Funds(name=form.name.data, dollars=form.dollars.data, total_mf_sector=form.total_mf_sector.data)
        db.session.add(mutual_fund)
        db.session.commit()
        flash("Congratulations, you added a Mutual Fund")
        return redirect(url_for('mutualFunds'))
    return render_template('mutualFunds.html',title='Mutual Funds', results=results, form=form, grow=True, data=True)


@app.route('/stocks',methods=['GET', 'POST'])
def view_stocks():
    results = Stocks.query.all()
    form = AddStocksForm()
    if form.validate_on_submit():
        stock = Stocks(ticker_symbol=form.ticker_symbol.data, legal_name=form.legal_name.data, total_shares=form.total_shares.data, current_price=form.current_price.data)
        db.session.add(stock)
        db.session.commit()
        flash("Congratulations, you added a Stock!")
        return redirect(url_for('view_stocks'))
    return render_template('stocks.html', title='Stocks', results=results, form=form, grow=True, data=True)
    
# @app.route('/test', methods=['GET'])
# def test():
#   results = Mutual_Funds.query.all()
#   print(results)
#   return render_template('test.html',title = 'TEST',results = results)