from flask import render_template, flash, redirect, session, url_for, request, g, make_response, send_file, abort, send_from_directory, Response, Markup
from flask.ext.login import login_user , logout_user , current_user , login_required
from app import app, db, login_manager
from .forms import LoginForm, RegisterForm
from .quizzes import *
from .models import User, UserRank, Level, Module, Quiz, Skill, QuestionLibrary as ql, AnswerLibrary as al
from config import basedir
from authomatic.adapters import WerkzeugAdapter
from config import authomatic #used for oauth2 stuff
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
                           title='LING SLEUTH')

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login_with_provider(provider_name):
    """
    Login handler, must accept both GET and POST to be able to use OpenID.
    """
    print "CONFIG info:\n{}".format(app.config["CONFIG"])
    # We need response object for the WerkzeugAdapter.
    response = make_response()

    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            # We need to update the user to get more info.
            result.user.update()
            handle_user(result)
            # TODO: register user if needed.
            app.logger.info("{0} is a logged in via {1}.".format(result.user.name, provider_name))
        # The rest happens inside the template.
        #result.user.data.x will return further user data
        username = User.query.filter_by(username=result.user.name).first()
        return render_template('login-test.html', result=result, user=username)

    # Don't forget to return the response.
    return response

@app.route('/login',methods=['GET','POST'])
def login():
    # Choose a login provider
    return render_template('login.html')



@app.route('/logout')
def logout():
    logout_user()
    flash("Bye for now!")
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

@app.errorhandler(404)
def not_logged_in(error):
    return 'You must be logged in to access this page', 404

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
    user = User.query.filter_by(username=current_user.username).first()
    if user is None:
        abort(404)
    # TODO: Add skills and diagnosis here...
    return render_template('profile.html',
                           title='Profile')

@app.route('/cases')
def cases():
    return render_template('cases.html',
                           title='Cases')

@app.route('/learn/<module>', methods=['GET', 'POST'])
def modules(module):
    quiz = quiz_dict[module]
    quiz = quiz()
    if request.method == 'POST' and quiz.validate():
        print quiz.score.incorrect, 'blah'
        if len(quiz.score.incorrect) == 0:
            flash('Nice work!')
            # return redirect(url_for('quiz_submission'))
            permissions = current_user.user_rank.permissions + current_user.level.permissions
            print permissions
            next_rank = UserRank.query.filter_by(permissions=(current_user.user_rank.permissions + 0x010)).first()
            # current_user.user_rank = next_rank
            # print next_rank, current_user.user_rank.permissions + 0x010
            print next_rank.permissions
            next_module = Module.query.filter_by(permissions=next_rank.permissions).first()
            return render_template('quiz_submission.html',
                                    aced=True,
                                    next_module = next_module)
        else:
            # calculate user's score by subtracting the points missed from the points total
            user_score = quiz.score.quiz_points
            for error in quiz.score.incorrect:
                print quiz.score.incorrect[error]
                # error_info = quiz.errors[error]
                user_score -= quiz.score.incorrect[error]
            user_perc = float(user_score) / float(quiz.score.quiz_points)
            if user_perc > quiz.score.passing:
                next_rank = UserRank.query.filter_by(permissions=(current_user.user_rank.permissions + 0x010)).first()
                print next_rank
                current_user.user_rank = next_rank
                next_module = Module.query.filter_by(permissions=next_rank.permissions).first()
            else:
                next_module = 'None'
            #render the quiz submission page
            return render_template('quiz_submission.html',
                                    aced=False,
                                    next_module=next_module,
                                    quiz=quiz.score.quiz,
                                    questions=quiz.score.questions,
                                    errors=quiz.errors,
                                    user_perc=user_perc,
                                    threshold=quiz.score.passing)
    elif request.method == 'POST':
        print quiz.errors
        print quiz.score.incorrect
        if [u'This field is required.'] in quiz.errors.values():
            pass
        
    module_list = Module.query.filter_by(module=module.title().lower()).first()
    # quiz_list = Quiz.query.filter_by(quiz=module_list.module).first()
    # blah = Blah(quiz_list.quiz)
    # quiz_form = quiz_dict['fitb']()
    # quiz_form = quiz_dict['fitb'](quiz_form)
    # quiz_form.start(quiz_list.quiz)#.start()

    return render_template('{0}.html'.format(module),
                            title=module.title(),
                            number=module_list.number,
                            # quiz=quiz_list,
                            # quiz_name=quiz_list.quiz,
                            # true=True,
                            # false=False,
                            # match=False,
                            form=quiz)#quiz_form)

@app.route('/quiz_submission')
def quiz_submission():
    return render_template('quiz_submission.html')


@app.route('/learn')
def learn():
    if current_user.is_anonymous() == True:
        return not_logged_in(NameError)

    user = User.query.filter_by(username=current_user.username).first()

    user_permissions = user.user_rank.permissions + user.level.permissions
    modules = Module.query.order_by(Module.permissions)
    return render_template('learn.html',
                           title='Learn',
                           user=user,
                           user_permissions=user_permissions,
                           modules=modules)

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


def handle_user(result):
    # is the user registered?
    registered_user = User.query.filter(User.username == result.user.name, User.email == result.user.email).first()
    # register if necessary...
    if not registered_user:
        registered_user = register_user(result)
    login_user(registered_user)

def register_user(result):
    user = User(username=result.user.name, provider=result.provider.name, email=result.user.email)
    db.session.add(user)
    db.session.commit()
    flash("You've been registered!")
    return user

if __name__ == '__main__':
    app.debug = True
    app.run()
