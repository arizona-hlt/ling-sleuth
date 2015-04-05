from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from secret import CONFIG
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#APPLICATION_ROOT = 'app'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'png', 'jpg', 'jpeg', 'json'])

WTF_CSRF_ENABLED = True
SECRET_KEY = 'poop'

authomatic = Authomatic(CONFIG, SECRET_KEY, report_errors=False)

#OPENID_PROVIDERS = [
#    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
#    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
