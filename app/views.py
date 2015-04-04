from flask import render_template, flash, redirect, session, url_for, request, g, make_response, send_file, abort, send_from_directory, Response, Markup
from flask.ext.login import login_user , logout_user , current_user , login_required
from app import app, db, login_manager
from .forms import LoginForm, RegisterForm
from .models import User
from config import basedir
import os
import logging

UPLOADS_DIR = os.path.join(basedir, app.config['UPLOAD_FOLDER'])


# who is the current user?
@app.before_request
def before_request():
    g.user = current_user

# for handling user data
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Welcome')


@app.route('/register' , methods=['GET','POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate():
        user = User(request.form['username'] , request.form['password'], request.form['email'])
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))

    return render_template('register.html', title ='Register', form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", form=form)
    if request.method == "POST":
        submitted_form = request.form

        username = submitted_form['username']
        password = submitted_form['password']
        # login and validate the user...
        registered_user = User.query.filter_by(username=username,password=password).first()
        if registered_user:
            app.logger.info("{0} is a registered user.".format(username))
            login_user(registered_user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            app.logger.info("{0} is not a registered user.".format(username))
            flash("There was a problem...")
            # TODO: change this form to

    return render_template('login.html',title ='Log in', form=form)



@app.route('/logout')
def logout():
    logout_user()
    flash("Bye for now!")
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

#@app.errorhandler(DatabaseError)
#def special_exception_handler(error):
#    return 'Database connection failed', 500


###Other stuff

@app.route('/about')
def about():
    return render_template('about.html',
                           title='About')

@app.route('/profile')
@login_required
def profile():
     return render_template('profile.html',
                           title='Profile')

@app.route('/cases')
def cases():
    return render_template('cases.html',
                           title='Cases')

@app.route('/learn')
def learn():
    return render_template('learn.html',
                           title='Learn')

@app.route('/knowledge')
@login_required
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
