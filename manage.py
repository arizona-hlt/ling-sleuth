#!venv/bin/python
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()


"""
python manage.py db init # initialize a database
python manage.py db migrate # for initial migration
python manage.py db upgrade # for subsequent migrations
python manage.py db --help
"""
