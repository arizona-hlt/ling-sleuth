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

    #Unsure if these are going to work.  Need a one-to-many (maybe many-to-many) relationship
    skill_id = db.Column(db.Integer,db.ForeignKey('skills.id'))
    case_id = db.Column(db.Integer,db.ForeignKey('cases.id'))


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
        return self.username


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
    #this is how many "permission points" this module is worth???
    increase = db.Column('increase',db.Integer)
    #this is the "skill" obtained by completing the module.  This would go on the skills page.
    skill = db.Column('skill',db.Text,index=True,unique=True)
    #would this be a many-to-one?
    case = db.relationship('Case',backref='module',lazy='dynamic')


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
    #SOMEHOW THIS GOT DELETED        


    def remove_module(self,module):
        mod_name = Module.query.filter_by(module=module).first()
        if mod_name is None:
            return "Module not found."
        db.session.delete(mod_name)
        db.session.commit()


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer,primary_key=True)
    quiz = db.Column('quiz',db.String(50),unique=True,index=True)
    permissions = db.Column('permissions',db.Integer)
    description = db.Column('description',db.Text)
    passed = db.Column('passed',db.Boolean)
    
    #refs
    skill_id = db.Column('skill',db.String(50),unique=True,index=True)
    question_id = db.Column('question',db.Integer,db.ForeignKey('questions.id'))

    def __init__(self,quiz,permissions,description):
        self.quiz = quiz
        self.permissions = permissions
        self.description = description
        self.passed = False


    def add_quiz(line):
        quiz_name = Quiz.query.filter_by(quiz=line[0]).first()
        #line[0] is the quiz name
        if quiz_name is None:
            quiz_name = Quiz(quiz=line[0],permissions=line[1],description=line[2])
        quiz_name.skill_id = Skill.query.filter_by(skill=line[3])
        db.session.add(quiz_name)
        db.session.commit()

    def add_question(question):
        question_id = Question_Library.query.filter_by(question=question).first()



class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer,primary_key=True)
    skill = db.Column('skill',db.String(50),unique=True,index=True)
    #not sure if this should be associated with passing a quiz/module or not.
    quiz_id = db.relationship('Quiz',backref='skill',lazy='dynamic')
    user_id = db.relationship('User',backref='skill',lazy='dynamic')

    def add_skill(skill,quiz):
        skill_set = Skill.query.filter_by(skill=skill).first()
        if skill_set is None:
            skill_set = Skill(skill=skill)
        skill_set.quiz_id = Quiz.query.filter_by(quiz=quiz)
        db.session.add(skill_set)
        db.session.commit()



class Question_Library(db.Model):
    __tablename__ = 'questions'
    question = db.Column('question',db.Text,unique=True,index=True)
    points = db.Column('points',db.Integer)
    #e.g. short answer, multiple choice, T/F, etc.
    q_type = db.Column('q_type',db.String(20))

    quiz_id = db.relationship('Quiz',backref='question',lazy='dynamic')
    #answers
    incorrect_answer_id = db.Column('incorr_answer',db.Integer, db.ForeignKey('answers.id'))
    correct_answer_id = db.Column('corr_answer',db.Integer, db.ForeignKey('answers.id'))

    def __init__(self,question,points,q_type):
        self.question = question
        self.points = points
        self.q_type = q_type


    def add_question(line):
        question_text = Question_Library.query.filter_by(question=line[2])
        if question_text is None:
            question_text = Question_Library(question=line[1],points=line[2],q_type=line[3])
        
        #adding answers
        for item in line[4:len(line)]:
            Answer_Library.add_answer(item)
        question_text.correct_answer_id = Answer_Library.query.filter_by(answer=line[4])
        for item in line[5:len(line)]:
            question_text.incorrect_answer_id = Answer_Library.query.filter_by(answer=item)

        #linking question to quiz
        quiz = Quiz.query.filter_by(line[0])
        quiz.add_question(line[1])
        db.session.add(question_text)
        db.session.commit()



class Answer_Library(db.Model):
    __tablename__ = 'answers'
    answer = db.Column('answer',db.Text,unique=True,index=True)

    #backref
    question = db.relationship('Question_Library',backref='answer',lazy='dynamic')

    def __init__(self,answer):
        self.answer = answer
        
    def add_answer(answer):
        answer_text = Answer_Library.query.filter_by(answer=answer).first()
        if answer_text is None:
            answer_text = Answer_Library(answer=answer)
        db.session.add(answer_text)
        db.session.commit()


class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer,primary_key=True)
    case_name = db.Column('case',db.String(100),unique=True,index=True)
    accepted = db.Column('accepted',db.Boolean)

    #one to many relationships - unsure how to do, one of below two ways? for each of the below fields
    module_id = db.Column(db.Integer,db.ForeignKey('modules.id'))
    #modules = db.relationship('Module',backref='case')

    quiz_id = db.Column(db.Integer,db.ForeignKey('quiz.id'))
    skill_id = db.Column(db.Integer,db.ForeignKey('skill.id'))


    def __init__(self,case_name):
        self.case_name = case_name


    def add_case(casefile_path):
        casefile = open('../cases/casefile_path','r').readlines()

        case = Case.query.filter_by(case_name=casefile[0]).first()
        if case is None:
            case = Case(case_name=casefile[0],accepted=False)

        FIELD = None

        for line in casefile[1:len(casefile):
            line = line.split('\t')

            if line[0] == '#':
                FIELD = line[1]
                continue

            if FIELD == 'MODULE':
                #pass 'module, rank, level, description' to this function
                Module.add_module(line[0],line[1],line[2],line[3])
                case.module_id = Module.query.filter_by(module=line[0]).first()

            if FIELD == 'SKILL':
                Skill.add_skill(line)
                case.skill_id = Skill.query.filter_by(skill=line)

            if FIELD == 'QUIZ':
                Quiz.add_quiz(line)

            if FIELD == 'QUESTION':
                Question_Library.add_question(line)

            else:
                continue








