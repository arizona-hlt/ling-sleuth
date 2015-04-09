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
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))


    def __init__(self,username,provider,email):
        self.username = username
        self.provider = provider
        self.email = email
        self.registered_on = datetime.utcnow()
        if self.rank is None:
            self.rank = Rank.query.filter_by(default=True).first()
        if self.level is None:
            self.level = Level.query.filter_by(default=True).first()

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
    __tablename__ = "ranks"
    id = db.Column('id', db.Integer,primary_key=True)
    rank = db.Column('rank',db.String(20), index=True, unique=True)
    default = db.Column('default',db.Boolean, default=False, index=True)
    permissions = db.Column('permissions',db.Integer)

    users = db.relationship('User', backref='rank', lazy='dynamic')


    def __init__(self, rank, permissions):
        self.rank = rank
        self.permissions = permissions

    #this should only be run once to populate the database with the desired ranks
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
                level = Rank(rank=r,permissions=self.user_ranks[r][0])
            # level.permissions = self.user_ranks[r][0]
            level.default = self.user_ranks[r][1]
            db.session.add(level)
        db.session.commit()


    def __repr__(self):
        return self.rank


class Level(db.Model):
    __tablename__ = "levels"
    id = db.Column('id', db.Integer,primary_key=True)
    level = db.Column('level', db.String(20),index=True, unique=True)
    default = db.Column('default',db.Boolean,default=False,index=True)
    permissions = db.Column('permissions',db.Integer)

    users = db.relationship('User',backref='level',lazy='dynamic')

    def __init__(self,level,permissions):
        self.level = level
        self.permissions = permissions

    #This should only be run once to populate the database with the desired levels
    @staticmethod
    def initialize_levels(self):

        #0x011 is the maximum value here - 17, allowing for a total of 17 levels between ranks
        #can be set to a lower hex
        level_max = 0x011



        for l in range(0x000,level_max):#self.rank_levels:
            l_name = l+0x001
            level = Level.query.filter_by(level=l_name).first()
            if level is None:
                level = Level(level=l_name, permissions=l)

            if l == 0x000:
                level.default = True
            else:
                level.default = False

            db.session.add(level)
        db.session.commit()


    def __repr__(self):
        return self.level




class Permissions:

    ANONYMOUS = 0x000
    #Users
    GUMSHOE = 0x001
    ASSISTANT_DETECTIVE = 0x011
    DETECTIVE = 0x021
    PERSONAL_INVESTIGATOR = 0x031
    SLEUTH = 0x041
    SUPER_SLEUTH = 0x051
    WATSON = 0x061
    SHERLOCK = 0x071
    #Maintainers
    DUMMY_TEST = 0x0d1
    INSTRUCTOR = 0x0e1
    ADMINISTRATOR = 0x0f1


    # def assign_module_permissions():



class Module(db.Model):  #holds dict, where modules are keys, val=list the length of # of modules
    __tablename__ = 'modules'
    id = db.Column(db.Integer,primary_key=True)
    module = db.Column('module',db.String(64),index=True,unique=True)
    permissions = db.Column('permissions',db.Integer)
    description = db.Column('description',db.Text,index=True,unique=True)

    def __init__(self,module):
        self.module = module

    # modules = {
    #         'Syntax'        :   [-1]*3,
    #         'Phonology'     :   [-1]*3,
    #         'Morphology'    :   [-1]*3,
    #         'Computational' :   [-1]*7
    # }

    @staticmethod
    def add_module(module,rank,level,description):
        mod_name = Module.query.filter_by(module=module).first()
        if mod_name is None:
            mod_name = Module(module=module)
        rank = Rank.query.filter_by(rank=rank).first()
        level = Level.query.filter_by(level=level).first()
        print(rank.permissions,level.permissions)
        # print(rank.query.filter('permissions'))
        # rank_permissions = rank.permissions
        # level_permissions = level.permissions
        mod_name.permissions = int(rank.permissions) + int(level.permissions)
        mod_name.description = description
        db.session.add(mod_name)
        db.session.commit()


    def remove_module(self,module):
        mod_name = Module.query.filter_by(module=module).first()
        if mod_name is None:
            return "Module not found."
        db.session.delete(mod_name)
        db.session.commit()
