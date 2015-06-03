from flask.ext.wtf import Form
from wtforms import TextField, StringField, HiddenField, PasswordField, SubmitField, SelectField
from wtforms.validators import *
from wtforms.fields.html5 import EmailField


class LoginInfo:

    def __init__(self):
        self.username = None
        self.password = None

class UserName(object):

    def __init__(self):
        # self.form = form
        pass

    def __call__(self,form,field):
        self.username = field.data
        form.login_info.username = field.data

class PassWord(object):

    def __init__(self):
        # self.form = form
        pass

    def __call__(self,form,field):
        self.password = field.data
        form.login_info.password = field.data

class LoginForm(Form):

    login_info = LoginInfo()
    # provider = SelectField(u'Log in with...', choices = [("google","Google"), ("gh","GitHub"), ("fb","FaceBook")], validators = [Required()])
    # username = StringField('Username', id='username', validators=[InputRequired("Forgetting something?")])
    # password = PasswordField('Password', id='password', validators=[Required()])
    # submit = SubmitField('Log in', id='login')

class RegisterForm(Form):

    login_info = LoginInfo()
    #name = StringField('Name', id='name')
    # username = StringField('Username', id='username', validators=[Required("Uh-oh! You forgot to choose a username.")])
    # password = PasswordField('Password', id='password', validators=[Required("Is it safe?  Is it secret?")])
    # email = EmailField('Email', id='email', validators=[Required("For a timely delivery of spam, of course..."), Email()])
    # submit = SubmitField('Register', id='register')

# class TraceForm(Form):
#     name = StringField('Tracer ID', id='tracer', validators=[Required()])
#     subject = StringField('Subject', id='subject')
#     project_id = StringField('Project ID', id='project', validators=[Required()])
#     data = HiddenField(id='trace-data')
#     submit = SubmitField('Get traces', id='dump-traces')

class CreateLogin():

    def __init__(self):
        pass


    def create(self):
        # login_form = LoginForm
        
        # setattr(login_form,'username',StringField('Username', id='username', validators=[InputRequired(),UserName(login_form)]))
        # setattr(login_form,'password',PasswordField('Password', id='password', validators=[InputRequired(),PassWord(login_form)]))
        # setattr(login_form,'submit',SubmitField('Log in', id='login'))

        register_form = RegisterForm

        setattr(register_form,'username',StringField('Username', id='username', validators=[InputRequired(),UserName()]))
        setattr(register_form,'password',PasswordField('Password', id='password', validators=[InputRequired(),PassWord()]))
        setattr(register_form,'submit',SubmitField('Register', id='register'))

        # login_form = login_form()
        register_form = register_form()

        # login_form.login_info.username = None
        # login_form.login_info.password = None
        register_form.login_info.username = None
        register_form.login_info.password = None        

        return register_form


# form_dict = {"login":LoginForm(),"register":RegisterForm()}

