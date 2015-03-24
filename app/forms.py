from flask.ext.wtf import Form
from wtforms import TextField, StringField, HiddenField, PasswordField, SubmitField
#from flask.ext.wtf import validators
from wtforms.validators import *
from wtforms.fields.html5 import EmailField

class LoginForm(Form):
    username = StringField('Username', id='username', validators=[InputRequired("Forgetting something?")])
    password = PasswordField('Password', id='password', validators=[Required()])
    submit = SubmitField('Log in', id='login')

class RegisterForm(Form):
    #name = StringField('Name', id='name')
    username = StringField('Username', id='username', validators=[Required("Uh-oh! You forgot to choose a username.")])
    password = PasswordField('Password', id='password', validators=[Required("Is it safe?  Is it secret?")])
    email = EmailField('Email', id='email', validators=[Required("For a timely delivery of spam, of course..."), Email()])
    submit = SubmitField('Reporting for duty!', id='register')

class TraceForm(Form):
    name = StringField('Tracer ID', id='tracer', validators=[Required()])
    subject = StringField('Subject', id='subject')
    project_id = StringField('Project ID', id='project', validators=[Required()])
    data = HiddenField(id='trace-data')
    submit = SubmitField('Get traces', id='dump-traces')
