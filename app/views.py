from flask import render_template, flash, redirect, session, url_for, request, g, make_response, send_file, abort, send_from_directory, Response, Markup
from flask.ext.login import login_user , logout_user , current_user , login_required
from app import app, db, login_manager
from .forms import CreateLogin
from .quizzes import *
from .special_login import *
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
        return render_template('login-success.html',
                                current_user=username)

    # Don't forget to return the response.
    return response

@app.route('/login',methods=['GET','POST'])
def login():
    #create the login form for administrators
    cl = CreateLogin()
    register_form = cl.create()

    if request.method == 'POST' and register_form.validate():
        print "YAYAYA"
        if User.query.filter_by(username=register_form.login_info.username).first() is not None:
            print "HUG?"
            flash("Username already taken")
        else:
            print register_form.login_info.username
            print register_form.login_info.password
            register_user(register_form.login_info.username,register_form.login_info.password)
            print "HDASFDS?D?SAF?"
            current_user.username = register_form.login_info.username
            return render_template('login-success.html',
                                    current_user=register_form.login_info.username)

    # elif request.method == 'POST' and login_form.validate():
    #     print "HSDAYDF"
    #     current_user.username = login_form.login_info.username
    #     return render_template('login-success.html',
    #                             current_user=login_form.login_info.username)

    # Choose a login provider
    return render_template('login.html',
                            # logform=login_form,
                            regform=register_form)



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

@app.errorhandler(404)
def insufficient_xp(error):
    return 'You must have more xp to access this content!', 404

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
    print current_user.user_rank
    user = User.query.filter_by(username=current_user.username).first()
    next_rank = UserRank.query.filter_by(permissions=current_user.user_rank.permissions+0x010).first()
    if user is None:
        abort(404)
    # TODO: Add skills and diagnosis here...
    return render_template('profile.html',
                           title='Profile',
                           next_rank=next_rank)

@app.route('/cases')
def cases():
    return render_template('cases.html',
                           title='Cases')


@app.route('/activity/text to spech/<data>')
def tts(data):
    return render_template('{}.html'.format(data),
                            title='Data File')

@app.route('/activity/<project>')
def projects(project):
    req_xp = Module.query.filter_by(module=project).first().permissions
    if current_user.xp < req_xp:
        return insufficient_xp(NameError)
    if current_user.xp == req_xp:
        added_xp = Module.query.filter_by(module=project).first().xp
        # flash('Nice work! +{0} XP'.format(added_xp))
        # set xp gain
        new_permissions = current_user.xp + added_xp
        current_user.xp = new_permissions

        # find the next rank
        next_rank = UserRank.query.filter_by(permissions=(current_user.user_rank.permissions + 0x010)).first()

        # work-around to check if the next rank was actually obtained
        if current_user.xp >= next_rank.permissions:
            current_user.user_rank = next_rank
            current_user.level = Level.query.filter_by(permissions=(current_user.xp-next_rank.permissions)).first()
        else:
            current_user.level = Level.query.filter_by(permissions=(current_user.xp-(next_rank.permissions-0x010))).first()

        db.session.add(current_user)
        db.session.commit()

    return render_template('{0}.html'.format(project),
                           title='{0}'.format(project))


@app.route('/activity')
def activity():
    if current_user.is_anonymous() == True:
        return not_logged_in(NameError)

    user = User.query.filter_by(username=current_user.username).first()
    #uncomment if there is a need to reset permissions
    # user.level = Level.query.filter_by(level="Level-1").first()
    # user.user_rank = UserRank.query.filter_by(user_rank="Gumshoe").first()
    # user.xp = 1
    # db.session.add(user)
    # db.session.commit()
    print user.user_rank.permissions
    print user.level.permissions
    user_permissions = user.user_rank.permissions + user.level.permissions
    modules = Module.query.order_by(Module.permissions)
    return render_template('activity.html',
                           title='Projects',
                           user=user,
                           user_permissions=user_permissions,
                           modules=modules)


@app.route('/learn/<module>', methods=['GET', 'POST'])
def modules(module):
    req_xp = Module.query.filter_by(module=module).first().permissions

    if current_user.xp < req_xp:
        return insufficient_xp(NameError)
    quiz = quiz_dict[module]
    # calls function in quizzes, which populates and instantiates the quiz class within the module
    cf = CreateForm(module)
    quiz = cf.create()
    # obtain the quiz object in the database to reference its fields
    quiz_object = Quiz.query.filter_by(quiz=quiz.score.quiz.quiz).first()
    # determines if enough XP has been earned in order to level up
    level_up = False

    # if submit AND no questions have been left blank
    if request.method == 'POST' and quiz.validate():

        # calculate user's score by subtracting the points missed from the points total
        user_score = quiz.score.quiz_points
        for error in quiz.score.incorrect:
            print error, quiz.score.quiz_points, quiz.score.incorrect[error]
            user_score -= quiz.score.incorrect[error]
        # calculate their percentage to compare against the required passing threshold
        user_perc = float(user_score) / float(quiz.score.quiz_points)

        if user_perc >= quiz.score.passing:

            # delete below line - currently used to reset user's xp to lowest level, 
            # prior to 'upgrade'; this is in place while testing
            # current_user.xp = 0x001
            if current_user.xp == req_xp:
                added_xp = Module.query.filter_by(module=module).first().xp
                flash('Nice work! +{0} XP'.format(added_xp))
                # set xp gain
                new_permissions = current_user.xp + added_xp
                current_user.xp = new_permissions

                # find the next rank
                next_rank = UserRank.query.filter_by(permissions=(current_user.user_rank.permissions + 0x010)).first()
                # work-around to check if the next rank was actually obtained
                if current_user.xp >= next_rank.permissions:
                    current_user.user_rank = next_rank
                    current_user.level = Level.query.filter_by(permissions=(current_user.xp-next_rank.permissions)).first()
                    level_up = True
                    flash('Level up!')
                else:
                    current_user.level = Level.query.filter_by(permissions=(current_user.xp-(next_rank.permissions-0x010))).first()

                # hack/ workaround - something better would be nice, but necessary to match 
                # the next module's permissions EXACTLY
                # subtract 1 from user's permissions to find the highest-permission module
                # they are qualified to look at
                permission_match = current_user.xp + 0x001
                next_module = None

                while next_module == None:
                    permission_match -= 0x001
                    next_module = Module.query.filter_by(permissions=permission_match).first()
            else:
                flash('Nice work!')
                next_module = module

        # if the module was passed the next module is the same module.
        else:
            next_module = module

        #save any changes to the current user's profile
        db.session.add(current_user)
        db.session.commit()

        #render the quiz submission page with all the variables
        return render_template('quiz_results.html',
                                level_up=level_up,
                                next_module=next_module,
                                quiz=quiz_object,
                                questions=quiz_object.questions,
                                errors=quiz.score.incorrect,
                                user_score=round(user_perc*100),
                                threshold=quiz.score.passing*100)
    
    # if a question has been left blank
    elif request.method == 'POST':
        if [u'This field is required.'] in quiz.errors.values():
            pass
    # obtain the module object to pass to the html page for the module
    module_list = Module.query.filter_by(module=module.title().lower()).first()


    return render_template('{0}.html'.format(module),
                            title=module.title(),
                            number=module_list.number,
                            form=quiz)#quiz_form)


@app.route('/quiz_results')
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

def register_user(username,password):
    user = User(username=username, password=password, xp=0.001, registration=True)
    db.session.add(user)
    db.session.commit()
    flash("You've been registered!")
    return user

if __name__ == '__main__':
    app.debug = True
    app.run()
