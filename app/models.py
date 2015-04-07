from hashlib import md5
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    provider = db.Column('provider', db.String(10))
    email = db.Column('email',db.String(50), unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)

    rank_id = db.Column(db.Integer, db.ForeignKey('ranks.id'))


    def __init__(self,username,provider,email):
        self.username = username
        self.provider = provider
        self.email = email
        self.registered_on = datetime.utcnow()
        if self.rank is None:
            self.rank = Rank.query.filter_by(default=True).first()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Rank(db.Model):
    __tablename__ = 'ranks'
    id = db.Column(db.Integer,primary_key=True)
    rank = db.Column('rank',db.String(20), index=True, unique=True)
    default = db.Column('default',db.Boolean, default=False, index=True)
    permissions = db.Column('permissions',db.Integer)
    users = db.relationship('User', backref='rank', lazy='dynamic')

    def __init__(self, rank):
        self.rank = rank

    @staticmethod
    def initialize_ranks(self):

        self.user_ranks = {
            'Anonymous':
                (Permissions.ANONYMOUS,False),
            'Gumshoe':
                (Permissions.GUMSHOE,True),
            'Assistant Detective':
                (Permissions.ASSISTANT_DETECTIVE, False),
            'Detective':
                (Permissions.DETECTIVE,False),
            'PI':
                (Permissions.PERSONAL_INVESTIGATOR,False),
            'Sleuth':
                (Permissions.SLEUTH,False),
            'Super Sleuth':
                (Permissions.SUPER_SLEUTH,False),
            'Watson':
                (Permissions.WATSON,False),
            'Sherlock':
                (Permissions.SHERLOCK,False)
        }

        for r in self.user_ranks:
            # try:
            level = Rank.query.filter_by(rank=r).first()
            if level is None:
                level = Rank(rank=r)
            level.permissions = self.user_ranks[r][0]
            level.default = self.user_ranks[r][1]
            db.session.add(level)
        db.session.commit()


    def __repr__(self):
        return '<Rank %r>' % (self.rank)

class Levels:

    q=1


class Permissions:

    ANONYMOUS = 0x000
    #Users
    GUMSHOE = 0x001
    ASSISTANT_DETECTIVE = 0x011
    DETECTIVE = 0x021
    PERSONAL_INVESTIGATOR = 0x031
    SLEUTH = 0x41
    SUPER_SLEUTH = 0x051
    WATSON = 0x061
    SHERLOCK = 0x071
    #Maintainers
    DUMMY_TEST = 0x0d1
    INSTRUCTOR = 0x0e1
    ADMINISTRATOR = 0x0f1


    # def assign_module_permissions():
        


class Skills:  #holds dict, where modules are keys, val=list the length of # of modules
    modules = {
            'Syntax'        :   [-1]*3,
            'Phonology'     :   [-1]*3,
            'Morphology'    :   [-1]*3,
            'Computational' :   [-1]*7
    }
