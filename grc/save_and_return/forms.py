from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from grc.utils.form_custom_validators import validateSecurityCode, validateReferenceNumber

from math import exp
import time
import requests
import threading

thread_local = threading.local()

class ReturnToYourApplicationForm(FlaskForm):
    reference = StringField('reference', validators=[DataRequired(message='Enter a valid reference number'), validateReferenceNumber])
    attempt = IntegerField('attempt', default=0)
    submit = SubmitField('Continue')
