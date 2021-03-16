from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.core import FloatField, IntegerField
from wtforms.fields.simple import HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class AddPortfoliosForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    initial_investment_amt = FloatField('initial_dollars', validators=[DataRequired()], default="1000")
    dollars_available = FloatField('dollars_available',validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddMutualFundsForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    initial_investment_amt = FloatField('initial_investment_amt',validators=[DataRequired()])
    # nav = FloatField('NAV',validators=[DataRequired()])
    shares_outstanding = FloatField('shares_outstanding',validators=[DataRequired()])
    dollars_available = FloatField('dollars_available',validators=[DataRequired()])
    dollars_invested = FloatField('dollars_invested')
    total_mf_sector = FloatField('total_mf_sector',validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class AddStocksForm(FlaskForm):
    ticker_symbol = StringField('ticker_symbol', validators=[DataRequired()])
    legal_name = StringField('legal_name', validators=[DataRequired()])
    current_share_price = FloatField('current_share_price',validators=[DataRequired()]) 
    total_number_shares = FloatField('total_number_shares',validators=[DataRequired()]) 
    shares_available = FloatField('shares_available',validators=[DataRequired()])
    initial_offering_price = FloatField('initial_offering_price',validators=[DataRequired()]) 
    sector_id = IntegerField('sector_id',validators=[DataRequired()]) 
    submit = SubmitField('Submit')

class AddSectorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchUsersForm(FlaskForm):
    username = StringField('username')
    submit = SubmitField('Submit')

class SearchStocksForm(FlaskForm):
    ticker_symbol = StringField('ticker_symbol')
    legal_name = StringField('legal_name')
    current_share_price = FloatField('current_share_price') 
    total_number_shares = FloatField('total_number_shares') 
    shares_available = FloatField('shares_available')
    initial_offering_price = FloatField('initial_offering_price') 
    sector_id = IntegerField('sector_id') 
    submit = SubmitField('Submit')

class SearchSectorsForm(FlaskForm):
    name = StringField('name')
    submit = SubmitField('Submit')

class SearchMutualFundsForm(FlaskForm):
    name = StringField('name')
    initial_investment_amt = FloatField('initial_investment_amt')
    nav = FloatField('NAV')
    shares_outstanding = FloatField('shares_outstanding')
    dollars_available = FloatField('dollars_available')
    dollars_invested = FloatField('dollars_invested')
    total_mf_sector = FloatField('total_mf_sector')
    submit = SubmitField('Submit')
    
class SearchHoldingsForm(FlaskForm):
    port_id_hold = IntegerField('Portfolio ID')
    mf_id_hold = IntegerField('Mutual Fund ID')
    # mf_shares = FloatField('Total Number of Shares',validators=[DataRequired()])
    mf_nav = FloatField('Current Mutual Fund NAV:')
    port_amount_invested = FloatField('Dollar Amount that you would like to invest')
    submit = SubmitField('Submit')
class SearchCFPForm(FlaskForm):
    mf_id = IntegerField('mf_id')
    stocks_id = IntegerField('stocks_id')
    total_shares = FloatField('Total Number of Shares')
    price_per_share = FloatField('price_per_share:')
    submit = SubmitField('Submit')

class AddHoldingsForm(FlaskForm):
    port_id_hold = IntegerField('Portfolio ID')
    mf_id_hold = IntegerField('Mutual Fund ID')
    mf_shares = FloatField('Total Number of Shares')
    mf_nav = FloatField('Current Mutual Fund NAV:')
    port_amount_invested = FloatField('Dollar Amount Invested')
    submit = SubmitField('Submit')

class Add_CFP_Form(FlaskForm):
    mf_id = IntegerField('mf_id')
    stocks_id = IntegerField('stocks_id')
    total_shares = FloatField('Total Number of Shares')
    price_per_share = FloatField('price_per_share:')
    submit = SubmitField('Submit')
    
