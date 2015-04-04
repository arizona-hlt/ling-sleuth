from flask import Flask
from flask.ext.login import LoginManager
import os
from config import basedir
import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.debug = True

app.config.from_object('config')

#manager = Manager(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

bootstrap = Bootstrap(app)

#sqlite3.connect(os.path.abspath("app.db"))
db = SQLAlchemy(app)
#is this the right spot?
#db.create_all()

from app import views, models # avoid circular references
