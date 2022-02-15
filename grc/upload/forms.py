from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField
from wtforms.validators import DataRequired
from grc.utils.form_custom_validators import MultiFileAllowed

class UploadForm(FlaskForm):
    documents = MultipleFileField('documents', validators=[MultiFileAllowed(['jpg', 'png', 'jpeg', 'tif', 'bmp', 'pdf'], message='You need to add allowed files') ])
    submit = SubmitField('Save and continue')

