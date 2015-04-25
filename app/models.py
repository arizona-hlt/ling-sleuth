import os
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

    user_rank_id = db.Column(db.Integer, db.ForeignKey('user_ranks.id'),nullable=True)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'),nullable=True)

    #Unsure if these are going to work.  Need a one-to-many (maybe many-to-many) relationship
    skill_id = db.Column(db.Integer,db.ForeignKey('skills.id'),nullable=True)
    # case_id = db.Column(db.Integer,db.ForeignKey('cases.id'))


    def __init__(self,username,provider=None,email=None):
        self.username = username
        self.provider = provider
        self.email = email
        self.registered_on = datetime.utcnow()
        if self.user_rank is None:
            self.user_rank = UserRank.query.filter_by(default=True).first()
        if self.level is None:
            self.level = Level.query.filter_by(default=True).first()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        try:
            self.username
            return False
        except:
            return True

    def set_anonymous(self):
        # self.username = 'Guest'
        self.user_rank = UserRank.query.filter_by(user_rank='Anonymous').first()
        self.level = Level.query.filter_by(default=True).first()

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return self.username


class UserRank(db.Model):
    __tablename__ = "user_ranks"
    id = db.Column('id', db.Integer,primary_key=True)
    user_rank = db.Column('user_rank',db.String(20), index=True, unique=True)
    default = db.Column('default',db.Boolean, default=False, index=True)
    permissions = db.Column('permissions',db.Integer)

    users = db.relationship('User', backref='user_rank', lazy='dynamic')


    def __init__(self, user_rank):
        self.user_rank = user_rank
        # self.permissions = permissions

    #this should only be run once to populate the database with the desired user_ranks
    @staticmethod
    def initialize_ranks(self):

        self.user_rank_list = {
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

        for r in self.user_rank_list:
            # try:
            level = UserRank.query.filter_by(user_rank=r).first()
            if level is None:
                level = UserRank(user_rank=r)
            level.permissions = self.user_rank_list[r][0]
            level.default = self.user_rank_list[r][1]
            db.session.add(level)
        db.session.commit()


    def __repr__(self):
        return self.user_rank


class Level(db.Model):
    __tablename__ = "levels"
    id = db.Column('id', db.Integer,primary_key=True)
    level = db.Column('level', db.String(20),index=True, unique=True)
    default = db.Column('default',db.Boolean,default=False,index=True)
    permissions = db.Column('permissions',db.Integer)

    users = db.relationship('User',backref='level',lazy='dynamic')

    def __init__(self,level):
        self.level = level
        # self.permissions = permissions

    #This should only be run once to populate the database with the desired levels
    @staticmethod
    def initialize_levels(self):

        #0x011 is the maximum value here - 17, allowing for a total of 17 levels between user_ranks
        #can be set to a lower hex
        level_max = 0x011



        for l in range(0x000,level_max):#self.rank_levels:
            l_name = 'Level-'+str(l+0x001)
            level = Level.query.filter_by(level=l_name).first()
            if level is None:
                level = Level(level=l_name)

            level.permissions = l
            if l == 0x000:
                level.default = True
            else:
                level.default = False
            print(level)
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





class Module(db.Model):  #holds dict, where modules are keys, val=list the length of # of modules
    __tablename__ = 'modules'
    id = db.Column(db.Integer,primary_key=True)
    module = db.Column('module',db.String(64),index=True,unique=True)
    number = db.Column('number',db.Integer)
    permissions = db.Column('permissions',db.Integer)
    description = db.Column('description',db.Text,index=True,unique=True)
    #this is how many "permission points" this module is worth???
    # increase = db.Column('increase',db.Integer)
    #this is the "skill" obtained by completing the module.  This would go on the skills page.
    skill = db.Column('skill',db.Text,index=True,unique=True)
    xp = db.Column('xp',db.Integer)
    #would this be a many-to-one?
    # case = db.relationship('Case',backref='module',lazy='dynamic')
    quizzes = db.relationship('Quiz',backref='module',lazy='dynamic')

    # def__init__(self):
    #     pass

    def __init__(self,module):
        self.module = module


    @staticmethod
    def add_module(module,number=None,user_rank=None,level=None,description=None,skill=None,xp=None):
        mod_name = Module.query.filter_by(module=module).first()
        if mod_name is None:
            mod_name = Module(module=module)
        if number:
            mod_name.number = number
        if user_rank:
            user_rank = UserRank.query.filter_by(user_rank=user_rank).first()
        if level:
            level = Level.query.filter_by(level=level).first()
        if user_rank and level:
            mod_name.permissions = int(user_rank.permissions) + int(level.permissions)
        # if increase:
        #     mod_name.increase = increase
        if description:
            mod_name.description = description
        if skill:
            mod_name.skill = skill
        if xp:
            mod_name.xp = xp
        db.session.add(mod_name)
        db.session.commit()


    @staticmethod
    def csv_upload():
        path = "app/mod_list.csv"
        f = open(path,'r').readlines()
        for l in f[1:]:     #skip header line
            line = l.strip().split('\t')

            module      = line[0]           if line[0] else None
            number      = int(line[1])      if line[1] else None
            user_rank   = line[2]           if line[2] else None
            level       = line[3]           if line[3] else None
            description = line[4]           if line[4] else None
            skill       = line[5]           if line[5] else None
            xp          = int(line[6],0)    if line[6] else None

            Module.add_module(module,number=number,user_rank=user_rank,level=level,
                            description=description,skill=skill,xp=xp)



    @staticmethod
    def remove_module(module):
        mod_name = Module.query.filter_by(module=module).first()
        if mod_name is None:
            return "Module not found."
        db.session.delete(mod_name)
        db.session.commit()


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer,primary_key=True)
    quiz = db.Column('quiz',db.String(50),unique=True,index=True)
    # permissions = db.Column('permissions',db.Integer)
    description = db.Column('description',db.Text)
    #this should be a percentage value specifying the percentage of correct questions to pass the quiz
    passing_threshold = db.Column('passing_threshold',db.Float)
    passed = db.Column('passed',db.Boolean,default=False)
    # xp = db.Column('xp',db.Integer)
    
    #refs
    # modules = db.relationship('Module',backref='quiz',lazy='dynamic')
    skills = db.relationship('Skill',backref='quiz',lazy='select',uselist=False)
    questions = db.relationship('QuestionLibrary',backref='quiz',lazy='dynamic')
    # skill_id = db.Column('skill',db.String(50),unique=True,index=True)
    module_id = db.Column(db.Integer,db.ForeignKey('modules.id'),nullable=True)
    # question_id = db.Column(db.Integer,db.ForeignKey('questions.id'))

    def __init__(self,quiz):
        self.quiz = quiz
        self.passed = False

    @staticmethod
    def add_quiz(quiz,permissions=None,description=None,passing_threshold=None,module=None):
        quiz_name = Quiz.query.filter_by(quiz=quiz).first()
        if quiz_name is None:
            quiz_name = Quiz(quiz=quiz)
        if permissions:
            quiz_name.permissions = permissions
        if description:
            quiz_name.description = description
        if passing_threshold:
            quiz_name.passing_threshold = passing_threshold
        # if xp:
        #     quiz_name.xp = xp
        if module:
            quiz_name.module = Module.query.filter_by(module=module).first()
        db.session.add(quiz_name)
        db.session.commit()

    @staticmethod
    def csv_upload():
        path = "app/quiz_list.csv"
        f = open(path,'r').readlines()
        for l in f[1:]:     #skip header line
            line = l.strip().split('\t')

            module              = line[0]           if line[0] else None
            quiz                = line[1]           if line[1] else None
            permissions         = int(line[2],0)      if line[2] else None
            description         = line[3]           if line[3] else None
            passing_threshold   = float(line[4])    if line[4] else None
            # q_type              = line[5]           if line[5] else None
            # xp          = int(line[6],0)    if line[6] else None

            Quiz.add_quiz(quiz=quiz,permissions=permissions,description=description,
                            passing_threshold=passing_threshold,module=module)
    # @staticmethod
    # def add_question(question):
    #     question_id = Question_Library.query.filter_by(question=question).first()
    # def __repr__(self):
    #     return self.module_id



class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer,primary_key=True)
    skill = db.Column('skill',db.String(100),unique=True,index=True)
    feature = db.Column('feature',db.String(50),unique=True,index=True)
    #not sure if this should be associated with passing a quiz/module or not.
    #ref
    quiz_id = db.Column(db.Integer,db.ForeignKey('quizzes.id'),nullable=True)
    user_id = db.relationship('User',backref='skill',lazy='dynamic')

    @staticmethod
    def add_skill(skill,quiz):
        skill_set = Skill.query.filter_by(skill=skill).first()
        if skill_set is None:
            skill_set = Skill(skill=skill)
        skill_set.quiz_id = Quiz.query.filter_by(quiz=quiz)
        db.session.add(skill_set)
        db.session.commit()


#Currently UNDER CONSTRUCTION
class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.Integer,primary_key=True)



class QuestionLibrary(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column('question_id',db.Integer,unique=True)
    question = db.Column('question',db.Text,unique=True,index=True)
    points = db.Column('points',db.Integer)
    #question type; options include: 'short' (answer), 'filb' (fill in the blank),
    # 'mc' (multiple choice),'tf' (true/false)
    q_type = db.Column('q_type',db.String(20))

    # quiz_id = db.relationship('Quiz',backref='question',lazy='dynamic')
    quiz_id = db.Column(db.Integer,db.ForeignKey('quizzes.id'),nullable=True)
    #answers
    answers = db.relationship('AnswerLibrary',backref='question',lazy='dynamic')

    def __init__(self,question_id):
        self.question_id = question_id
        # self.points = points
        # self.q_type = q_type

    @staticmethod
    def add_question(question_id,question=None,points=None,q_type=None,quiz=None):
        question_text = QuestionLibrary.query.filter_by(question_id=question_id).first()
        if question_text is None:
            question_text = QuestionLibrary(question_id=question_id)
        if question:
            question_text.question = question
        if points:
            question_text.points = points
        if q_type:
            question_text.q_type = q_type
        if quiz:
            question_text.quiz = Quiz.query.filter_by(quiz=quiz).first()
        db.session.add(question_text)
        db.session.commit()

        #adding answers
        # for item in line[4:len(line)]:
        #     Answer_Library.add_answer(item)
        # question_text.correct_answer_id = Answer_Library.query.filter_by(answer=line[4])
        # for item in line[5:len(line)]:
        #     question_text.incorrect_answer_id = Answer_Library.query.filter_by(answer=item)

        # #linking question to quiz
        
        # quiz.add_question(line[1])
        # db.session.add(question_text)
        # db.session.commit()
    @staticmethod
    def csv_upload():
        path = "app/question_list.csv"
        f = open(path,'r').readlines()
        for l in f[1:]:     #skip header line
            line = l.strip().split('\t')

            module      = line[0]           if line[0] else None
            quiz        = line[1]           if line[1] else None
            question_id = int(line[2])      if line[2] else None
            question    = line[3]           if line[3] else None
            points      = int(line[4])      if line[4] else None
            q_type      = line[5]           if line[5] else None
            # xp          = int(line[6],0)    if line[6] else None

            QuestionLibrary.add_question(question_id=question_id,question=question,points=points,
                                        q_type=q_type,quiz=quiz)


    @staticmethod
    def remove_question(question):
        question_text = QuestionLibrary.query.filter_by(question=question).first()
        if question_text is None:
            return "Question not found."
        db.session.delete(question_text)
        db.session.commit()


class AnswerLibrary(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column('answer_id',db.Integer,unique=True)
    answer = db.Column('answer',db.Text,unique=True,index=True)
    truth_value = db.Column('truth_value',db.Boolean)

    question_id = db.Column(db.Integer,db.ForeignKey('questions.id'),nullable=True)

    #backref
    # question = db.relationship('Question_Library',backref='answer',lazy='dynamic')

    def __init__(self,answer_id):
        self.answer_id = answer_id
        
    @staticmethod
    def add_answer(answer_id,answer=None,truth_value=None,question_id=None):
        answer_text = AnswerLibrary.query.filter_by(answer_id=answer_id).first()
        if answer_text is None:
            answer_text = AnswerLibrary(answer_id=answer_id)
        if answer:
            answer_text.answer = answer
        if truth_value:
            answer_text.truth_value = truth_value
        if question_id:
            answer_text.question = QuestionLibrary.query.filter_by(question_id=question_id).first()
        db.session.add(answer_text)
        db.session.commit()

    @staticmethod
    def csv_upload():
        path = "app/answer_list.csv"
        f = open(path,'r').readlines()
        for l in f[1:]:     #skip header line
            line = l.strip().split('\t')

            module          = line[0]           if line[0] else None
            quiz            = line[1]           if line[1] else None
            answer_id       = int(line[2])      if line[2] else None
            answer          = line[3]           if line[3] else None
            truth_value     = int(line[4])      if line[4] else None
            question_id     = int(line[5])       if line[5] else None
            # xp          = int(line[6],0)    if line[6] else None

            AnswerLibrary.add_answer(answer_id=answer_id,answer=answer,truth_value=truth_value,
                                        question_id=question_id)


    @staticmethod
    def remove_answer(answer_id):
        answer_text = AnswerLibrary.query.filter_by(answer_id=answer_id).first()
        if answer_text is None:
            return "Answer not found."
        db.session.delete(answer_text)
        db.session.commit()



#Currently UNDER CONSTRUCTION
class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer,primary_key=True)
#     case_name = db.Column('case',db.String(100),unique=True,index=True)
#     accepted = db.Column('accepted',db.Boolean)

#     #one to many relationships - unsure how to do, one of below two ways? for each of the below fields
#     module_id = db.Column(db.Integer,db.ForeignKey('modules.id'))
#     #modules = db.relationship('Module',backref='case')

#     quiz_id = db.Column(db.Integer,db.ForeignKey('quiz.id'))
#     skill_id = db.Column(db.Integer,db.ForeignKey('skill.id'))


#     def __init__(self,case_name):
#         self.case_name = case_name


#     def add_case(casefile_path):
#         casefile = open('../cases/casefile_path','r').readlines()

#         case = Case.query.filter_by(case_name=casefile[0]).first()
#         if case is None:
#             case = Case(case_name=casefile[0],accepted=False)

#         FIELD = None

#         for line in casefile[1:len(casefile)]:
#             line = line.split('\t')

#             if line[0] == '#':
#                 FIELD = line[1]
#                 continue

#             if FIELD == 'MODULE':
#                 #pass 'module, user_rank, level, description' to this function
#                 Module.add_module(line[0],line[1],line[2],line[3])
#                 case.module_id = Module.query.filter_by(module=line[0]).first()

#             if FIELD == 'SKILL':
#                 Skill.add_skill(line)
#                 case.skill_id = Skill.query.filter_by(skill=line)

#             if FIELD == 'QUIZ':
#                 Quiz.add_quiz(line)

#             if FIELD == 'QUESTION':
#                 Question_Library.add_question(line)

#             else:
#                 continue

#Currently UNDER CONSTRUCTION
class Skill_Track(db.Model):
    __tablename__ = 'skill_tracks'
    id = db.Column(db.Integer,primary_key=True)






