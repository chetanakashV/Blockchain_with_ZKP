
from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, SubmitField, validators, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired

class  ViewReportForm(Form):
    username=StringField('Username',[validators.Length(min=4,max=25)])

class SignupUser(Form):
    username =StringField('Userame',[validators.Length(min=4,max=25)])
    # password =StringField('Password',[validators.Length(min=4,max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    submit =SubmitField('Signup')

class SignIn(Form):
    username =StringField('Userame',[validators.Length(min=4,max=25)])
    # password =StringField('Password',[validators.Length(min=4,max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me =BooleanField('Remember me')
    submit =SubmitField('Login')

class AddReportForm(Form):
    report = TextAreaField('Report', [validators.length(min=8, max=200)])


class  ViewTransactionForm(Form):
    username=StringField('Username',[validators.Length(min=4,max=25)])


class SendReportForm(Form):
    recipient= StringField('Recipient Username', [validators.Length(min=4, max=25)])
    report = TextAreaField('Report', [validators.length(min=8, max=200)])
    # report = SelectField('Report', choices=[] ,validate_choice=False, validators=[InputRequired()])
    # print("Inside forms.py" ,report.data)
    submit =SubmitField('Send Report')
    