from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired, Email
from grc.utils.form_custom_validators import validateSecurityCode, validateReferenceNumber

class ReturnToYourApplicationForm(FlaskForm):
    reference = StringField('reference', validators=[DataRequired(message='Enter a valid reference number'), validateReferenceNumber])
    submit = SubmitField('Continue')


class ValidateCodeForm(FlaskForm):
    code = StringField('code', validators=[DataRequired(message='A valid code is required'), validateSecurityCode])
    submit = SubmitField('Continue')
