from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from grc.utils.form_custom_validators import validateSecurityCode, validateReferenceNumber

class ReturnToYourApplicationForm(FlaskForm):
    reference = StringField('reference', validators=[DataRequired(message='Enter a valid reference number'), validateReferenceNumber])
    submit = SubmitField('Continue')
