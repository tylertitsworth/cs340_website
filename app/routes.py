
from flask import render_template, flash, redirect, url_for,json, Markup,request
from flask_login import current_user
from flask_googlecharts import GoogleCharts,PieChart
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Query,query
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import true 
from app import app, db, charts
from app.forms import AddPortfoliosForm, AddSectorForm, LoginForm, RegistrationForm, EditProfileForm, AddMutualFundsForm,AddStocksForm, SearchUsersForm,AddHoldingsForm,Add_CFP_Form, SearchCFPForm, SearchHoldingsForm, SearchMutualFundsForm, SearchSectorsForm, SearchStocksForm
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
        portfolio = Portfolios()
        add_form.populate_obj(portfolio)
        # portfolio = Portfolios(name=add_form.name.data, initial_dollars=add_form.initial_dollars.data, dollars_invested_port=add_form.dollars_invested_port.data, user_id=current_user.get_id())
        portfolio.user_id = current_user.get_id()
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
        form.populate_obj(results)
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
    # return render_template('index.html', title='Home Page')

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

    user_search_results = User.query.all()
    port_search_results = Portfolios.query.all()
    hold_search_results = Holdings.query.all()
    mf_search_results = Mutual_Funds.query.all()
    cfp_search_results = current_fund_price.query.all()
    stock_search_results = Stocks.query.all()
    sector_search_results = Sectors.query.all()
    
    user_search_form=SearchUsersForm()
    port_search_form = SearchUsersForm()
    holdings_search_form = SearchHoldingsForm
    mf_search_form = SearchMutualFundsForm()
    stock_search_form = SearchStocksForm()
    cfp_search_form = SearchCFPForm()
    sector_search_form = SearchSectorsForm()
    
    if form.validate_on_submit():
        user_results = User.query.filter_by(username=form.username.data)

    return render_template('admin.html',title='Admin',user_results=user_results,
    port_results = port_results, hold_results = hold_results,mf_results = mf_results,
    cfp_results = cfp_results, stonk_results =  stonk_results,sector_results=sector_results, user_data = True, port_data = True,
    hold_data = True, mf_data = True, cfp_data = True, stonk_data = True, sector_data = True, user_search_form=user_search_form,
    port_search_form = port_search_form, holdings_search_form = holdings_search_form, mf_search_form = mf_search_form, stock_search_form = stock_search_form,
    cfp_search_form = cfp_search_form, sector_search_form = sector_search_form)

@app.route('/mutualFunds',methods=['GET', 'POST'])
def mutualFunds():
    mf_results = Mutual_Funds.query.all()
    add_form = AddMutualFundsForm()
    if add_form.validate_on_submit():
        mutual_fund = Mutual_Funds()
        add_form.populate_obj(mutual_fund)
        mutual_fund.nav = add_form.dollars_available.data / add_form.shares_outstanding.data
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
        form.populate_obj(results)
        results.nav = form.dollars_available.data / form.shares_outstanding.data
        # results.name=form.name.data
        # results.dollars=form.dollars.data
        # results.total_mf_sector=form.total_mf_sector.data
        db.session.commit()
        flash("Congratulations, you edited a Mutual Fund")
        return redirect(url_for('mutualFunds'))
    return render_template('editMutualFunds.html', title="Edit Funds",results=results.name,form=form,fund=True)

@app.route('/stocks',methods=['GET', 'POST']) 
def stocks():
    stonk_results = Stocks.query.all()
    form = AddStocksForm()
    if form.validate_on_submit():
        new_stock = Stocks()
        form.populate_obj(new_stock)
        db.session.add(new_stock)
        db.session.commit()
        flash("Congratulations, you added a Stock!")
        return redirect(url_for('stocks'))
    return render_template('stocks.html', title='Stocks', stonk_results=stonk_results, form=form, grow=True, stonk_data=True, ent_page=True,edit_delete=True)

@app.route('/editStocks/<int:id>',methods=['GET', 'POST'])
def editStocks(id):
    results = Stocks.query.filter_by(id=id).first_or_404()
    form = AddStocksForm(obj=results)
    if form.validate_on_submit():
        form.populate_obj(results)
        db.session.commit()
        flash("Congratulations, you edited a Stock!")
        return redirect(url_for('stocks'))
    return render_template('editStocks.html', title="Edit Stocks",results=results.legal_name,form=form,fund=True)

@app.route('/deleteStocks/<int:id>',methods=['GET', 'POST'])
def deleteStocks(id):
    Stocks.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Congratulations, you deleted a Stock!")
    return redirect(url_for('stocks'))

@app.route('/addMutualFundtoPortfolio/<int:id>', methods=['GET', 'POST'])
def addMutualFundtoPortfolio(id):
    results = Mutual_Funds.query.all()
    port_form = AddHoldingsForm()
    return render_template('addMutualFund.html', title="Add a Mutual Fund to a Portfolio", results=results, data=True, pid=id, add_mf=False,port_form=port_form)

@app.route('/addMutualFund/<int:id>/<int:pid>', methods=['GET', 'POST', 'PATCH'])
def addMutualFund(id, pid):
    results = Mutual_Funds.query.filter_by(id=id)
    input_nav = None
    for i in results:
        input_nav = i.nav
    print(input_nav)
    port_form = AddHoldingsForm(port_id_hold=pid, mf_id_hold=id,mf_nav=input_nav)
    if port_form.validate_on_submit():
        new_holdings = Holdings()
        print(port_form.port_amount_invested)
        port_form.populate_obj(new_holdings)
        new_holdings.mf_shares = port_form.port_amount_invested.data / port_form.mf_nav.data
        db.session.add(new_holdings)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addMutualFund.html', title="Add a Mutual Fund to a Portfolio", results=results, data=True, pid=id, add_mf=True,port_form=port_form)
    
    
    # db.session.commit()
    # print("Mutual Fund", Mutual_Funds.query.filter_by(id=id), " added to Portfolio ", Portfolios.query.filter_by(id=pid), "!")
    # flash("Mutual Fund Added!")
    # add_form = AddPortfoliosForm()
    # results = Portfolios.query.filter_by(user_id=current_user.get_id())
    # Mresults = Mutual_Funds.query.filter_by(portfolio_id = pid)
    # return redirect(url_for('index'))
    # return render_template('index.html', title="Home Page", Mresults=Mresults, results=results, add_form=add_form, grow=True, data=True, view=True)

@app.route('/viewMutualFunds/<int:id>', methods=['GET', 'POST'])
def viewMutualFunds(id):
    add_form = AddPortfoliosForm()
    results = Portfolios.query.filter_by(user_id=current_user.get_id())
    Mresults = Mutual_Funds.query.filter(Mutual_Funds.port_rel.any(id=id))
    return render_template('index.html', title="Home Page", Mresults=Mresults, results=results, add_form=add_form, grow=True, data=True, view=True)

@app.route('/addHoldings/<int:id>', methods=['GET', 'POST'])
def addHoldings(id):
    current_mf =  Mutual_Funds.query.filter_by(id=id)
    results = Stocks.query.all()
    return render_template('addtoHoldings.html', title="Add a Mutual Fund to a Portfolio", results=results, stonk_data=True, test_cfp=True, current_mf=current_mf,id = id)

@app.route('/addtoHoldings/<int:id>', methods=['GET', 'POST'])
def addtoHoldings(id):
    current_mf =  Mutual_Funds.query.filter_by(id=id)
    add_form = Add_CFP_Form()
    results = Stocks.query.all()
    if add_form.validate_on_submit():
        new_cfp = current_fund_price()
        add_form.populate_obj(new_cfp)
        db.session.add(new_cfp)
        db.session.commit()
        return redirect(url_for('current_fund_price'))
    return render_template('addtoHoldings.html', title="Mutual Funds", results=results, stonk_data=True, test_cfp=True, current_mf=current_mf)

@app.route('/viewHoldings/<int:id>', methods=['GET'])
def viewHoldings(id):
    add_form = AddMutualFundsForm()
    results = Mutual_Funds.query.all()
    Mresults = Stocks.query.filter(Stocks.mf_rel.any(id=id)) 
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
    my_chart = PieChart("my_chart",options={"title":'Sector Breakdown', 
                                            "width": 600,
                                            "height": 400, 
                                            "is3D": True})
    my_chart.add_column("string", "Sector")
    my_chart.add_column("number", "Dollars Invested")
    charts.register(my_chart)
    sect_names = []
    stock_sect_vals = []
    stock_sect_out = Stocks.query.all()
    for stonk in stock_sect_out:
        stock_sect_vals.append(stonk.current_share_price)
        sect_x = Sectors.query.filter_by(id=stonk.id)
        if sect_x is not None:
            for n in sect_x:
                sect_names.append(n.name)
        print(stonk)

    stock_sect_combo = list(map(list,zip(sect_names,stock_sect_vals)))
    print(stock_sect_combo)
    my_chart.add_rows(stock_sect_combo)
    return render_template('graphSectors.html', title='Mutual Fund Sector Breakdown', my_chart=my_chart, stock_sects=True,sect_out = stock_sect_combo)



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
    return render_template('sectors.html', title='Sectors', sector_results=sector_results, form=form, sector_data=True, admin_thead = False, admin_td = False, entity_home=True)

@app.route('/editSectors/<int:id>',methods=['GET', 'POST'])
def editSectors(id):
    results = Sectors.query.filter_by(id=id).first_or_404()
    form = AddSectorForm(obj=results)
    if form.validate_on_submit():
        form.populate_obj(results)
        db.session.commit()
        flash("Congratulations, you edited a Sector!")
        return redirect(url_for('sectors'))
    return render_template('editStocks.html', title="Edit Stocks",results=results,form=form,fund=True)

@app.route('/deleteSectors/<int:id>',methods=['GET', 'POST'])
def deleteSectors(id):
    Sectors.query.filter_by(id=id).delete()
    flash("Congratulations, you deleted a Sector!")
    db.session.commit()
    return redirect(url_for('sectors'))

@app.route('/currentFundPrice/<int:id>' ,methods=['GET','POST'])
def currentFundPrice(id):
    results = current_fund_price.query.filter_by(mf_id=id)
    form = Add_CFP_Form(mf_id = id)
    stonk_results = Stocks.query.all()
    if form.validate_on_submit():
        new_cfp = current_fund_price()
        form.populate_obj(new_cfp)
        db.session.add(new_cfp)
        db.session.commit()
        flash("Congratulations, you added a Stock!")
        return redirect(url_for('currentFundPrice'))
    return render_template('currentFundPrice.html', title='Currrent Fund Price', cfp_results=results, form=form, add_cfp=True, data=True, stonk_data=True, stonk_results=stonk_results, ent_page=False,  edit_delete=False,mf_id=id)


@app.route('/editCFP/<int:id>' ,methods=['GET','POST'])
def editCFP(id):
    results = current_fund_price.query.filter_by(id=id)
    form = Add_CFP_Form(obj=results)
    if form.validate_on_submit():
        form.populate_obj(results)
        db.session.commit()
        return redirect(url_for('currentFundPrice'))
    return render_template('editCFP.html', title="Edit Current Fund Price",results=results,form=form)



@app.route('/deleteCFP/<int:id>' ,methods=['GET','POST'])
def deleteCFP(id):
    result = current_fund_price.query.filter_by(id=id)
    curr_mf_id = 0
    for x in result:
        curr_mf_id = x.mf_id
        print(x)
    current_fund_price.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/editUser' ,methods=['GET','POST'])
def editUser():
    return redirect(url_for('login'))

@app.route('/deleteUser' ,methods=['GET','POST'])
def deleteUser():
    return redirect(url_for('login'))


@app.route('/admin_holdings' ,methods=['GET','POST'])
def admin_holdings():
    hold_results = Holdings.query.all()
    form = AddStocksForm()
    if form.validate_on_submit():
        new_stock = Stocks(ticker_symbol=form.ticker_symbol.data, legal_name=form.legal_name.data, total_shares_circulation=form.total_shares.data, current_price=form.current_price.data)
        db.session.add(new_stock)
        db.session.commit()
        flash("Congratulations, you added a Stock!")
    return render_template('admin_holdings.html', title='Holdings Table ',hold_results=hold_results, hold_data=True)



@app.route('/viewPortfolioHoldings/<int:id>' ,methods=['GET','POST'])
def viewPortfolioHoldings(id):
    hold_results = Holdings.query.filter_by(port_id_hold = id).all()
    print(f"hold_results {hold_results}")
    form = AddStocksForm()
    if form.validate_on_submit():
        new_stock = Stocks(ticker_symbol=form.ticker_symbol.data, legal_name=form.legal_name.data, total_shares_circulation=form.total_shares.data, current_price=form.current_price.data)
        db.session.add(new_stock)
        db.session.commit()
        flash("Congratulations, you added a Stock!")
    return render_template('viewPortfolioHoldings.html', title='Portfolio Holdings',hold_results=hold_results, hold_data=True)