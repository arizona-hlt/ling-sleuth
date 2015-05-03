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
        # obtains the quiz object/table in the database
        self.quiz = Quiz.query.filter_by(quiz=quiz).first()
        # obtains the list of questions associated with the quiz
        self.questions = self.quiz.questions #QuestionLibrary.query.filter_by(quiz=self.quiz.quiz_id).all() #self.quiz.questions
        # print self.questions
        # loops through each question to get each question's point value
        # add to get the total number of points for the quiz
        self.quiz_points = 0
        for question in self.questions:
            # print question
            self.quiz_points += question.points
        # obtains the point threshold / score at which someone can still pass the quiz, e.g. '0.90'
        self.passing = self.quiz.passing_threshold
        self.incorrect = {}



class CorrectAnswer(object):

    def __init__(self,a_id,q_id):
        # answer to question
        self.answer             = al.query.filter_by(answer_id=a_id).first().answer
        # id # of question
        self.question_id        = q_id    #QuestionLibrary.query.filter_by(question_id=q_id).first().question_id
        # the points that the question is worth; this is passed back with the Question ID if wrong
        self.question_points    = QuestionLibrary.query.filter_by(question_id=q_id).first().points

    def __call__(self, form, field):

        re.IGNORECASE

        if re.match(self.answer, field.data) is None:
            # if there is no match between the true answer and the submitted answer (i.e. they got it wrong)
            # raise a validation error that passes back the question_id and points to views.py
            # raise ValidationError('',[self.question_id, self.question_points])
            form.score.incorrect[self.question_id] = self.question_points


class Ngrams(Form):
    # instantiate the Score class, which contains quiz-specific variables for reference during quiz assessment
    quiz = 'n-grams'
    score = Score(quiz)
    
    trigrams = StringField('What do you call an n-gram of three elements?',
                            # Every time the form is submitted, the validators for each question (field)
                            # are checked to see if they return a true value, or if an error is raised.
                            validators=[Required(),
                                        #answer_id, question_id (as in database) are required arguments
                                        CorrectAnswer(1,1)])

    nchar_bigrams_total = StringField('How many character bigrams are in the word "abracadabra"?',
                                      # id='2',
                                      validators=[Required(),
                                                  CorrectAnswer(2,2)])

    nchar_bigrams_distinct = StringField('How many DISTINCT character bigrams are in the word "abracadabra"?',
                                      # id='3',
                                      validators=[Required(),
                                                  CorrectAnswer(3,3)])
    
    # creates the submit button
    submit = SubmitField('Submit Answers', id='grade')



class PartOfSpeech(Form):

    quiz = 'part of speech'
    score = Score(quiz)

    np = StringField('What does NP stand for?',
                     # id='np',
                     validators=[Required(),
                                 CorrectAnswer(4,4)])

    submit = SubmitField('Submit Answers',
                        id='grade')



# referenced in views.py, enabling it to access the quiz class based on the module name
# We will need to change this when / if we have multiple quizzes per module.
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


