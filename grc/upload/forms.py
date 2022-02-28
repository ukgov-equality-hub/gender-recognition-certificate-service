from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from grc.utils.form_custom_validators import MultiFileAllowed, FileSizeLimit

class UploadForm(FlaskForm):
    documents = MultipleFileField('documents', validators=[MultiFileAllowed(['jpg', 'png', 'jpeg', 'tif', 'bmp', 'pdf'], message='You need to add allowed files'), FileSizeLimit(10) ])
    submit = SubmitField('Save and continue')

class DeleteForm(FlaskForm):
    section = HiddenField('section', validators=[DataRequired(message='Field is required')])
    file = HiddenField('file', validators=[DataRequired(message='Field is required')])
    redirect_route = HiddenField('redirect_route', validators=[DataRequired(message='Field is required')])
    submit = SubmitField('Remove')
