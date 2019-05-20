from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class EntryForm(FlaskForm):
    entry = StringField('Entry')
    submit = SubmitField('Ask GrandPy')
