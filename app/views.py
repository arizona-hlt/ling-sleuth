from flask import render_template, flash, redirect, session, url_for, request, g, make_response, send_file, send_from_directory, Response
import os
#from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
from .forms import LoginForm
from .models import User
from config import basedir

UPLOADS_DIR = os.path.join(basedir, app.config['UPLOAD_FOLDER'])

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Welcome')

@app.route('/login')
def login():
    return render_template('login.html',
                           title='Login')

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

#@app.errorhandler(DatabaseError)
#def special_exception_handler(error):
#    return 'Database connection failed', 500

@app.route('/about')
def about():
    return render_template('about.html',
                           title='About')

@app.route('/cases')
def cases():
    return render_template('cases.html',
                           title='Cases')

@app.route('/learn')
def learn():
    return render_template('learn.html',
                           title='Learn')

@app.route('/knowledge')
def knowledge():
    return render_template('knowledge.html',
                           title='Unlocked Skillz!')

@app.route('/downloads/<filename>')
def serve_file(filename):
    return Response(open(os.path.join(UPLOADS_DIR, filename), 'rb').read(),
                       mimetype="text/plain",
                       headers={"Content-Disposition":
                                    "attachment;filename={0}".format(filename)})

if __name__ == '__main__':
    app.debug = True
    app.run()
