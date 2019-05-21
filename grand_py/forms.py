from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):
    entry = TextAreaField('entry',
                           validators=[DataRequired()])
    submit = SubmitField('Ask GrandPy')

