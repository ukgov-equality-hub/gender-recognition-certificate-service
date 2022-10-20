from flask_wtf import FlaskForm
from wtforms import StringField


class ReferenceNumberForm(FlaskForm):
    reference_number = StringField()
