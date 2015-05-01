#!venv/bin/python
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db
from app.models import User, UserRank, Level, Module, Quiz, QuestionLibrary, AnswerLibrary

migrate = Migrate(app, db)

manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, UserRank=UserRank, Level=Level, Module=Module, Quiz=Quiz, QuestionLibrary=QuestionLibrary, AnswerLibrary=AnswerLibrary)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# # class Reboot():
# 	def reboot():
# 		print 'Rebooting...'
# 		UserRank.initialize_ranks(UserRank)
# 		Level.initialize_levels(Level)
# 		Module.csv_upload()
# 		Quiz.csv_upload()
# 		QuestionLibrary.csv_upload()
# 		AnswerLibrary.csv_upload()
#		User.add_admin()
# manager.add_command('reboot', Reboot())

# # class Refresh():
# def refresh():
# 	print 'Refreshing...'
# 	Module.csv_upload()
# 	Quiz.csv_upload()
# 	QuestionLibrary.csv_upload()
# 	AnswerLibrary.csv_upload()
#	User.add_admin()
# manager.add_command('refresh', Refresh())

if __name__ == '__main__':
    manager.run()



"""
python manage.py db init # initialize a database
python manage.py db migrate # for initial migration
python manage.py db upgrade # for subsequent migrations
python manage.py db --help
"""
