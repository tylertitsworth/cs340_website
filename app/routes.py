
from flask import render_template, flash, redirect, url_for,json, Markup, request
from flask_login import current_user
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query,query
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import true 
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddMutualFundsForm, AddStocksForm, AddPortfoliosForm,AddSectorForm
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User, Mutual_Funds, Stocks, Portfolios,current_fund_price, Holdings,Sectors
from werkzeug.urls import url_parse
from datetime import date, datetime, timedelta

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    results = Portfolios.query.filter_by(user_id = current_user.get_id())
    add_form = AddPortfoliosForm()
    if add_form.validate_on_submit():
        portfolio = Portfolios(name=add_form.name.data, initial_dollars=add_form.dollars.data, user_id=current_user.get_id())
        db.session.add(portfolio)
        db.session.commit()
        flash("Congratulations, you added a Portfolio")
        return redirect(url_for('index'))
    return render_template('index.html', title='Portfolios', results=results, add_form=add_form, grow=True, data=True)

@app.route('/editPortfolio/<int:id>',methods=['GET', 'POST'])
def editPortfolio(id):
    results = Portfolios.query.filter_by(id=id).first_or_404()
    form = AddPortfoliosForm(obj=results)
    if form.validate_on_submit():
        results.name=form.name.data
        results.dollars=form.dollars.data
        db.session.commit()
        flash("Congratulations, you edited a Portfolio")
        return redirect(url_for('index'))
    return render_template('editPortfolios.html', title="Edit Portfolio",results=results.name,form=form,fund=True)

@app.route('/deletePortfolio/<int:id>',methods=['GET', 'POST'])
def deletePortfolio(id):
    Mutual_Funds.query.filter_by(portfolio_id=id).update({"portfolio_id" : None}, synchronize_session='evaluate', update_args=None)
    Portfolios.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Congratulations, you deleted a Portfolio!")
    return redirect(url_for('index'))
    return render_template('index.html', title='Home Page')

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

@app.route('/admin',methods=['GET', 'POST'])
def admin():
    user_results = User.query.all()
    port_results = Portfolios.query.all()
    hold_results = Holdings.query.all()
    mf_results = Mutual_Funds.query.all()
    cfp_results = current_fund_price.query.all()
    stonk_results = Stocks.query.all()
    sector_results = Sectors.query.all()
    return render_template('admin.html',title='Admin',user_results=user_results,
    port_results = port_results, hold_results = hold_results,mf_results = mf_results,
    cfp_results = cfp_results, stonk_results =  stonk_results,sector_results=sector_results, user_data = True, port_data = True,
    hold_data = True, mf_data = True, cfp_data = True, stonk_data = True, sector_data = True)

@app.route('/mutualFunds',methods=['GET', 'POST'])
def mutualFunds():
    mf_results = Mutual_Funds.query.all()
    add_form = AddMutualFundsForm()
    if add_form.validate_on_submit():
        mutual_fund = Mutual_Funds(name=add_form.name.data, initial_investment_amt=add_form.initial_investment_amt.data, dollars_available= add_form.dollars_available.data, dollars_invested=add_form.dollars_invested.data,  mf_share_price = add_form.mf_share_price.data, total_mf_sector=add_form.total_mf_sector.data)
        db.session.add(mutual_fund)
        db.session.commit()
        flash("Congratulations, you added a Mutual Fund")
        return redirect(url_for('mutualFunds'))
    return render_template('mutualFunds.html',title='Mutual Funds', mf_results=mf_results, add_form=add_form,grow=True, data=True)

@app.route('/deleteMutualFunds/<int:id>',methods=['GET', 'POST'])
def deleteMutualFunds(id):
    Mutual_Funds.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Congratulations, you deleted a Mutual Fund")
    return redirect(url_for('mutualFunds'))


@app.route('/editMutualFunds/<int:id>',methods=['GET', 'POST'])
def editMutualFunds(id):    
    results = Mutual_Funds.query.filter_by(id=id).first_or_404()
    form = AddMutualFundsForm(obj=results)
    if form.validate_on_submit():
        results.name=form.name.data
        results.dollars=form.dollars.data
        results.total_mf_sector=form.total_mf_sector.data
        db.session.commit()
        flash("Congratulations, you edited a Mutual Fund")
        return redirect(url_for('mutualFunds'))
    return render_template('editMutualFunds.html', title="Edit Funds",results=results.name,form=form,fund=True)

@app.route('/stocks',methods=['GET', 'POST']) 
def view_stocks():
    stonk_results = Stocks.query.all()
    form = AddStocksForm()
    if form.validate_on_submit():
        new_stock = Stocks(ticker_symbol=form.ticker_symbol.data, legal_name=form.legal_name.data, total_shares_circulation=form.total_shares.data, current_price=form.current_price.data)
        db.session.add(new_stock)
        db.session.commit()
        flash("Congratulations, you added a Stock!")
        return redirect(url_for('view_stocks'))
    return render_template('stocks.html', title='Stocks', stonk_results=stonk_results, form=form, grow=True, stonk_data=True)

@app.route('/editStocks/<int:id>',methods=['GET', 'POST'])
def editStocks(id):
    results = Stocks.query.filter_by(id=id).first_or_404()
    form = AddStocksForm(obj=results)
    if form.validate_on_submit():
        results.ticker_symbol=form.ticker_symbol.data
        results.legal_name=form.legal_name.data 
        results.total_shares=form.total_shares.data 
        results.current_price=form.current_price.data
        db.session.commit()
        flash("Congratulations, you edited a Stock!")
        return redirect(url_for('view_stocks'))
    return render_template('editStocks.html', title="Edit Stocks",results=results.legal_name,form=form,fund=True)

@app.route('/deleteStocks/<int:id>',methods=['GET', 'POST'])
def deleteStocks(id):
    Stocks.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Congratulations, you deleted a Stock!")
    return redirect(url_for('view_stocks'))

@app.route('/addMutualFundtoPortfolio/<int:id>', methods=['GET', 'POST'])
def addMutualFundtoPortfolio(id):
    # id = portfolio id
    results = Mutual_Funds.query.filter_by(portfolio_id=None)
    return render_template('addMutualFund.html', title="Add a Mutual Fund to a Portfolio", results=results, data=True, pid=id)

@app.route('/addMutualFund/<int:id>/<int:pid>', methods=['GET', 'POST', 'PATCH'])
def addMutualFund(id, pid):
    # id = Mutual Fund id
    # pid = Portfolio id
    Mutual_Funds.query.filter_by(id=id).update({"portfolio_id" : pid}, synchronize_session='evaluate', update_args=None)
    db.session.commit()
    print("Mutual Fund", Mutual_Funds.query.filter_by(id=id), " added to Portfolio ", Portfolios.query.filter_by(id=pid), "!")
    flash("Mutual Fund Added!")
    add_form = AddPortfoliosForm()
    results = Portfolios.query.filter_by(user_id=current_user.get_id())
    Mresults = Mutual_Funds.query.filter_by(portfolio_id = pid)

    return render_template('index.html', title="Home Page", Mresults=Mresults, results=results, add_form=add_form, grow=True, data=True, view=True)

@app.route('/viewMutualFunds/<int:id>', methods=['GET', 'POST'])
def viewMutualFunds(id):
    # id = portfolio id
    add_form = AddPortfoliosForm()
    results = Portfolios.query.filter_by(user_id=current_user.get_id())
    Mresults = Mutual_Funds.query.filter_by(portfolio_id = id)
    return render_template('index.html', title="Home Page", Mresults=Mresults, results=results, add_form=add_form, grow=True, data=True, view=True)

@app.route('/addHoldings/<int:id>', methods=['GET', 'POST'])
def addHoldings(id):
    # id = mfund id
    results = Stocks.query.all()
    return render_template('addtoHoldings.html', title="Add a Mutual Fund to a Portfolio", results=results, data=True, pid=id)

@app.route('/addtoHoldings/<int:id>/<int:pid>', methods=['GET', 'POST'])
def addtoHoldings(id,pid):
    # id = mfund id
    # id = PortfoliosMutual_funds(id=id)
    # Stocks.query.filter_by(id=id).update({"mfid" : pid}, synchronize_session='evaluate', update_args=None)
    # Mutual_Funds.query.filter_by(id=pid).update({"sid" : id}, synchronize_session='evaluate', update_args=None)
    # db.session.commit()
    cfp = current_fund_price(mf_id=pid,stocks_id=id)
    db.session.add(cfp)
    db.session.commit()
    print(current_fund_price.query.all())
    print("Stocks", Stocks.query.filter_by(id=id), " added to Mutual Fund ", Mutual_Funds.query.filter_by(id=pid), "!")
    flash("Stock Added!")
    add_form = AddPortfoliosForm()
    results = Mutual_Funds.query.filter_by(id=pid)
    # return redirect(url_for('view_stocks'))
    return render_template('mutualFunds.html', title="Mutual Funds", results=results, data=True)

@app.route('/viewHoldings/<int:id>', methods=['GET'])
def viewHoldings(id):
    add_form = AddMutualFundsForm()
    results = Mutual_Funds.query.all()
    Mresults = Stocks.query.filter(Stocks.mf_rel.any(id=id)) #filter_by(mfid = id)
    #Mresults=current_fund_price.query.filter_by(mf_id=id)
    return render_template('mutualFunds.html', title="Mutual Funds", Mresults=Mresults, results=results, add_form=add_form, grow=True, data=True, view=True)


@app.route('/test', methods=['GET','POST'])
def test():
    something = text("SELECT * FROM stocks;")
    tst = db.session.execute(something)
    results = []
    qTest1 = db.session.query(Mutual_Funds)
    qTest2 = db.session.query(Stocks)
    qTest3 = db.session.query(current_fund_price)
    # qTest4 = db.session.query(Mutual_Funds)
    mf_tests = [qTest1,qTest2,qTest3]
    for q in mf_tests:
        print(render_query(q,db.session))
        results.append(render_query(q,db.session))
    print(current_fund_price.query.all())

    return render_template('test.html',title='test',results=results)

def render_query(statement, db_session):
    """
    Generate an SQL expression string with bound parameters rendered inline
    for the given SQLAlchemy statement.
    WARNING: This method of escaping is insecure, incomplete, and for debugging
    purposes only. Executing SQL statements with inline-rendered user values is
    extremely insecure.
    Based on http://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
    """
    if isinstance(statement, Query):
        statement = statement.statement
    dialect = db_session.bind.dialect

    class LiteralCompiler(dialect.statement_compiler):
        def visit_bindparam(
            self, bindparam, within_columns_clause=False, literal_binds=False, **kwargs
        ):
            return self.render_literal_value(bindparam.value, bindparam.type)

        def render_array_value(self, val, item_type):
            if isinstance(val, list):
                return "{}".format(
                    ",".join([self.render_array_value(x, item_type) for x in val])
                )
            return self.render_literal_value(val, item_type)

        def render_literal_value(self, value, type_):
            if isinstance(value, int):
                return str(value)
            elif isinstance(value, (str, date, datetime, timedelta)):
                return "'{}'".format(str(value).replace("'", "''"))
            elif isinstance(value, list):
                return "'{{{}}}'".format(
                    ",".join(
                        [self.render_array_value(x, type_.item_type) for x in value]
                    )
                )
            return super(LiteralCompiler, self).render_literal_value(value, type_)

    return LiteralCompiler(dialect, statement).process(statement)

@app.route('/graphSectors', methods=['GET','POST'])
def graphSectors():
    labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'Communications']
    values = [
        967.67, 1190.89, 1079.75, 1349.19,
        2328.91, 2504.28, 2873.83, 4764.87,
        4349.29, 6458.30, 9907, 16297]
    colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    pie_values = values
    pie_labels = labels
    return render_template('graphSectors.html', title='Mutual Fund Sector Breakdown', max=17000, set=zip(values, labels, colors))



@app.route('/sectors' ,methods=['GET','POST'])
def sectors():
    sector_results = Sectors.query.all()
    form = AddSectorForm()
    if form.validate_on_submit():
        new_sector = Sectors(name=form.name.data)
        db.session.add(new_sector)
        db.session.commit()
        flash("Congratulations, you added a Sector!")
        return redirect(url_for('sectors'))
    return render_template('sectors.html', title='Sectors', sector_results=sector_results, form=form, grow=True, sector_data=True)

@app.route('/currentFundPrice' ,methods=['GET','POST'])
def currentFundPrice():
    results = Stocks.query.all()
    form = AddStocksForm()
    if form.validate_on_submit():
        new_stock = Stocks(ticker_symbol=form.ticker_symbol.data, legal_name=form.legal_name.data, total_shares=form.total_shares.data, current_price=form.current_price.data)
        db.session.add(new_stock)
        db.session.commit()
        flash("Congratulations, you added a Stock!")
        return redirect(url_for('currentFundPrice'))
    return render_template('currentFundPrice.html', title='Currrent Fund Price', results=results, form=form, grow=True, data=True)

@app.route('/editUser' ,methods=['GET','POST'])
def editUser():
    return redirect(url_for('login'))

@app.route('/deleteUser' ,methods=['GET','POST'])
def deleteUser():
    return redirect(url_for('login'))

@app.route('/viewPortfolioHoldings' ,methods=['GET','POST'])
def viewPortfolioHoldings():
    hold_results = Holdings.query.all()
    form = AddStocksForm()
    if form.validate_on_submit():
        new_stock = Stocks(ticker_symbol=form.ticker_symbol.data, legal_name=form.legal_name.data, total_shares_circulation=form.total_shares.data, current_price=form.current_price.data)
        db.session.add(new_stock)
        db.session.commit()
        flash("Congratulations, you added a Stock!")
    return render_template('viewPortfolioHoldings.html', title='Portfolio Holdings',hold_results=hold_results, hold_data=True)