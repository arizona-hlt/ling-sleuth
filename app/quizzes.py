from flask.ext.wtf import Form
import re
from flask import render_template
from random import randrange
from wtforms.form import BaseForm
from wtforms import TextField, StringField, HiddenField, PasswordField, SubmitField, SelectField
from wtforms.validators import ValidationError, Required, Regexp
from wtforms.fields.html5 import EmailField
# from wtforms.ext.sqlalchemy.orm import model_form
from app.models import Module, Quiz, QuestionLibrary, AnswerLibrary as al

# al = AnswerLibrary()

class Score:

    def __init__(self,quiz):
        self.quiz = Quiz.query.filter_by(quiz=quiz).first()
        self.questions = self.quiz.questions
        self.quiz_points = 0
        for question in self.questions:
            self.quiz_points += question.points
        self.passing = self.quiz.passing_threshold



class CorrectAnswer(object):

    def __init__(self,answer,q_id):
        self.answer             = answer
        self.question_id        = QuestionLibrary.query.filter_by(question_id=q_id).first().question_id
        self.question_points    = QuestionLibrary.query.filter_by(question_id=q_id).first().points

    def __call__(self, form, field):

        re.IGNORECASE

        if re.match(self.answer, field.data) is None:
            raise ValidationError([self.question_id,self.question_points])


class Ngrams(Form):
    #name = StringField('Name', id='name')
    quiz = 'n-grams'
    score = Score(quiz)

    trigrams = StringField('What do you call an n-gram of three elements?',
                            id='1',
                            validators=[Required("HINT: An n-gram with two elements is a bigram."),
                                        # Regexp('trigram.?',flags=re.IGNORECASE,message=u'Incorrect'),
                                        CorrectAnswer(al.query.filter_by(answer_id=1).first().answer,1)])

    nchar_bigrams_total = StringField('How many character bigrams are in the word "abracadabra"?',
                                      id='2',
                                      validators=[Required("You forgot to count those character bigrams!"),
                                                  # Regexp('10|ten',flags=re.IGNORECASE,message=u'Incorrect'),
                                                  CorrectAnswer(al.query.filter_by(answer_id=2).first().answer,2)])

    nchar_bigrams_distinct = StringField('How many DISTINCT character bigrams are in the word "abracadabra"?',
                                      id='3',
                                      validators=[Required("Forgettin' somethin'?"),
                                                  # Regexp("7|seven",flags=re.IGNORECASE,message=u'Incorrect'),
                                                  CorrectAnswer(al.query.filter_by(answer_id=3).first().answer,3)])
    # print 'SCOREs: ', score.user_score
    submit = SubmitField('Did I pass?', id='grade')#,validators=[Redirect(score.user_score)])



class PartOfSpeech(Form):

    quiz = 'part of speech'
    score = Score(quiz)

    np = StringField('What does NP stand for?',
                     id='np',
                     validators=[Required("Unanswered Question!"),
                                 # Regexp("noun phrase",flags=re.IGNORECASE,message=u'Incorrect'),
                                 CorrectAnswer(al.query.filter_by(answer_id=3).first().answer,3)])

    submit = SubmitField('Submit Answers',
                        id='grade')#,validators=[Redirect(score.user_score)])




quiz_dict = {'n-grams':Ngrams,u'part of speech':PartOfSpeech}

#,'fitb':FillInTheBlank}


# class FillInTheBlank(Form):

#     # form = BaseForm({
#     #     'name':StringField('What do you call an n-gram of three elements?',
#     #                         id='num_char_bigrams',
#     #                         validators=[Required("HINT: An n-gram with two elements is a bigram.")]),
#     #     'blah':SubmitField('Did I pass?', id='grade')
#     #     })
#     def __call__(self,quiz):
#         self.quiz = Quiz.query.filter_by(quiz=quiz).first()

#         self.questions = Question_Library.query.filter_by(quiz=self.quiz).all()
#         # print self.questions
#         for q in questions:
#             bound_field = StringField(q.question,
#                                 id=str(q.question_id),
#                                 validators=[Required("Fill in all the blanks!")])#.bind(form=self,name='blah')
#         #     self._unbound_fields.append(("internal_field", unbound_field))
#         #     bound_field = unbound_field.bind(self, 'X'+str(q.question_id), translations=self._get_translations())
#         #     self._fields['X'+str(q.question_id)] = bound_field
#             self.__dict__['X'+str(q.question_id)] = bound_field
#             setattr(self,'X'+str(q.question_id),bound_field)

#         # submit = SubmitField('Did I pass?', id='grade')
#         # self.__dict__['submit'] = SubmitField('Did I pass?', id='grade')
#         # print self._unbound_fields


