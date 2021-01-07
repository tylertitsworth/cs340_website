from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    # see this variable
    variable = {'pointer': 'value'}
    # variable store for a loop
    var_stores = [
        {
            'parameter1': {'pointer': '1'},
            'parameter2': 'text1'
        },
        {
            'parameter1': {'pointer': '2'},
            'parameter2': 'text2'
        }
    ]
    # notice the variable inclusions in list form on the render_template() function
    return render_template('index.html', title='Home', variable=variable, var_stores=var_stores)

@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index')) #This will send a logged in user to the given route
    return render_template('login.html', title='Sign In', form=form)