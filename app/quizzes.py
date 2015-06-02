from flask.ext.wtf import Form
import re
from flask import render_template
from random import randrange
from wtforms.form import BaseForm
from wtforms import TextField, StringField, HiddenField, PasswordField, SubmitField, SelectField
from wtforms.validators import ValidationError, Required, Regexp
from wtforms.fields.html5 import EmailField
from wtforms.ext.appengine.db import model_form
from app.models import Module, Quiz, QuestionLibrary, AnswerLibrary as al

# al = AnswerLibrary()

class Score:

    def __init__(self,quiz):
        # obtains the quiz object/table in the database
        self.quiz = Quiz.query.filter_by(quiz=quiz).first()
        # obtains the list of questions associated with the quiz
        self.questions = self.quiz.questions 
        # loops through each question to get each question's point value
        # add to get the total number of points for the quiz
        self.quiz_points = 0
        for question in self.questions:
            self.quiz_points += question.points
        # obtains the point threshold / score at which someone can still pass the quiz, e.g. '0.90'
        self.passing = self.quiz.passing_threshold
        # dictionary that holds the information of the question if that question is incorrect
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


class Frequency(Form):

    quiz='frequency'
    score = Score(quiz)
    # score.score()

# Must manually create a physical class; inherits from the Form metaclass
class Ngrams(Form):

    # must manually specify the name of the quiz
    quiz = 'n-grams'
    score = Score(quiz)
    # score.score()

    # Unfortunately, including this function (below) breaks the code - something with having an __init__
    # function does not allow the Fields to be bound.  Looks like we'll have to create a separate class
    # for each quiz manually, and manually copy the above two lines, changing the name of the quiz
    #  def __init__(self,quiz):
    #      self.quiz = quiz
    #      self.score = Score(self.quiz)

class PartOfSpeech(Form):

    quiz = 'part of speech'
    score = Score(quiz)
    # score.score()


class CreateForm():

    def __init__(self,module):
        self.quiz = module

    def create(self):
        #obtain the reference for the quiz class; do not instatiate yet
        new_form = quiz_dict[self.quiz]
        # counter for num of questions - to change the q name each iteration
        i=1
        # quiz database object - to be able to access its db fields
        quiz_object = Quiz.query.filter_by(quiz=self.quiz).first()

        # list of all question objectss associated with the quiz
        questions = quiz_object.questions

        for question in questions:

            # question id
            q_id = question.question_id
            # answer id
            a_id = al.query.filter_by(question_id=q_id).first().answer_id
            # set a Field attribute - critically prior to class instatiation
            setattr(new_form, 'q{0}'.format(i), StringField(question.question,validators=[Required(),CorrectAnswer(a_id,q_id)]))
            # increment variable naming counter
            i+=1
        # set the submit button field
        setattr(new_form,'submit', SubmitField('Submit Answers'))
        # instantiate the class AFTER the field attributes have been declared (Above);
        # can't have any functions (even init) within the class, or fields become unbounded
        new_form = new_form()
        # reset dict of incorrect questions
        new_form.score.incorrect = {}
        # return the instatiated class object to views.py
        return new_form


# referenced in views.py, enabling it to access the quiz class based on the module name
# We will need to change this when / if we have multiple quizzes per module.
quiz_dict = {'n-grams':Ngrams,u'part of speech':PartOfSpeech,u'frequency':Frequency}






