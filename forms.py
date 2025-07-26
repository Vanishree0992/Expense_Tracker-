from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, BooleanField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(LoginForm):
    email = StringField('Email')

class TransactionForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired()])
    currency = SelectField('Currency', choices=[('USD','USD'),('EUR','EUR')])
    date = DateField('Date', validators=[DataRequired()])
    description = StringField('Description')
    recurring = BooleanField('Recurring?')
    receipt = FileField('Receipt Image')
    category = SelectField('Category', coerce=int)
    account = SelectField('Account', coerce=int)
    submit = SubmitField('Save')
