from flask.ext.wtf import Form
import re
from flask import render_template
from random import randrange
from wtforms.form import BaseForm
from wtforms import TextField, StringField, HiddenField, PasswordField, SubmitField, SelectField
from wtforms.validators import ValidationError, Required, Regexp
from wtforms.fields.html5 import EmailField



class AdminLogin(Form):

	username = StringField('Username',
							validators=[Required()])

	password = PasswordField('Password',
							validators=[Required()])

	submit = SubmitField('Special User Login')