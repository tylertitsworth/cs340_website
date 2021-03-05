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
    initial_dollars = FloatField('initial_dollars', validators=[DataRequired()], default="1000")
    dollars_invested_port = FloatField('dollars_invested_port', validators=[DataRequired()], default="1000")
    submit = SubmitField('Submit')

class AddMutualFundsForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    initial_investment_amt = FloatField('initial_investment_amt',validators=[DataRequired()])
    dollars_available = FloatField('dollars_available',validators=[DataRequired()])
    dollars_invested = FloatField('dollars_invested',validators=[DataRequired()])
    mf_share_price = FloatField('mf_share_price',validators=[DataRequired()])
    total_mf_sector = FloatField('total_mf_sector',validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class AddStocksForm(FlaskForm):
    ticker_symbol = StringField('ticker_symbol', validators=[DataRequired()])
    legal_name = StringField('legal_name', validators=[DataRequired()])
    total_shares_circulation = FloatField('total_shares_circulation',validators=[DataRequired()]) 
    total_shares_available = FloatField('total_shares_available',validators=[DataRequired()])
    initial_price = FloatField('initial_price',validators=[DataRequired()]) 
    current_price = FloatField('current_price',validators=[DataRequired()]) 
    submit = SubmitField('Submit')

class AddSectorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Submit')

# class AddHoldingsForm(FlaskForm):
#     port_id_hold = 
#     mf_id_hold =
#     amount_invested = 
#     total_shares_invested =  
#     initial_share_price  =
#     current_share_price =