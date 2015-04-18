from flask.ext.wtf import Form
from wtforms import TextField, StringField, HiddenField, PasswordField, SubmitField, SelectField
from wtforms.validators import *
from wtforms.fields.html5 import EmailField

class Ngrams(Form):
    #name = StringField('Name', id='name')
    trigrams = StringField('What do you call an n-gram of three elements?',
                            id='num_char_bigrams',
                            validators=[Required("HINT: An n-gram with two elements is a bigram.")])
    nchar_bigrams_total = StringField('How many character bigrams are in the word "abracadabra"?',
                                      id='num_char_bigrams',
                                      validators=[Required("You forgot to count those character bigrams!")])

    nchar_bigrams_distinct = StringField('How many DISTINCT character bigrams are in the word "abracadabra"?',
                                      id='num_char_bigrams',
                                      validators=[Required("Forgetting something?")])
    submit = SubmitField('Did I pass?', id='grade')


quiz_dict = {'n-grams':Ngrams}
