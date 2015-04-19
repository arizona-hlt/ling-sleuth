from flask.ext.wtf import Form
import re
from wtforms.form import BaseForm
from wtforms import TextField, StringField, HiddenField, PasswordField, SubmitField, SelectField
from wtforms.validators import *
from wtforms.fields.html5 import EmailField
# from wtforms.ext.sqlalchemy.orm import model_form
from app.models import Module, Quiz, QuestionLibrary, AnswerLibrary




class Ngrams(Form):
    #name = StringField('Name', id='name')
    
    trigrams = StringField('What do you call an n-gram of three elements?',
                            id='num_char_bigrams',
                            validators=[Required("HINT: An n-gram with two elements is a bigram."),
                                        Regexp('trigram.*',flags=re.IGNORECASE,message=u'Incorrect')])
    nchar_bigrams_total = StringField('How many character bigrams are in the word "abracadabra"?',
                                      id='num_char_bigrams',
                                      validators=[Required("You forgot to count those character bigrams!"),
                                                  Regexp('10|ten',flags=re.IGNORECASE,message=u'Incorrect')])

    nchar_bigrams_distinct = StringField('How many DISTINCT character bigrams are in the word "abracadabra"?',
                                      id='num_char_bigrams',
                                      validators=[Required("Forgettin' somethin'?"),
                                                  Regexp("7|seven",flags=re.IGNORECASE,message=u'Incorrect')])
    submit = SubmitField('Did I pass?', id='grade')



class PartOfSpeech(Form):

    np = StringField('What does NP stand for?',
                     id='np',
                     validators=[Required("Unanswered Question!"),
                                 Regexp("[N|n]oun [P|p]hrase",message=u'Incorrect')])

    submit = SubmitField('Submit Answers',id='grade')




quiz_dict = {'n-grams':Ngrams,u'part of speech':PartOfSpeech}

#,'fitb':FillInTheBlank}


# class FillInTheBlank(Form):

#     form = BaseForm({
#         'name':StringField('What do you call an n-gram of three elements?',
#                             id='num_char_bigrams',
#                             validators=[Required("HINT: An n-gram with two elements is a bigram.")]),
#         'blah':SubmitField('Did I pass?', id='grade')
#         })
    # def start(self,quiz):
    #     self.quiz = Quiz.query.filter_by(quiz=quiz).first()

    #     self.questions = Question_Library.query.filter_by(quiz=self.quiz).all()
    #     # print self.questions
    #     for q in self.questions:
    #         bound_field = StringField(q.question,
    #                             id=str(q.question_id),
    #                             validators=[Required("Fill in all the blanks!")])#.bind(form=self,name='blah')
    #     #     self._unbound_fields.append(("internal_field", unbound_field))
    #     #     bound_field = unbound_field.bind(self, 'X'+str(q.question_id), translations=self._get_translations())
    #     #     self._fields['X'+str(q.question_id)] = bound_field
    #         self.__dict__['X'+str(q.question_id)] = bound_field
    #         setattr(self,'X'+str(q.question_id),bound_field)

    #     self.__dict__['submit'] = SubmitField('Did I pass?', id='grade')
    #     print self._unbound_fields


