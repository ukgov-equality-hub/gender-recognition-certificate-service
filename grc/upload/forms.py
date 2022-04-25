from flask_wtf import FlaskForm
from wtforms import MultipleFileField, BooleanField, HiddenField
from wtforms.validators import DataRequired
from grc.utils.form_custom_validators import MultiFileAllowed, FileSizeLimit


class UploadForm(FlaskForm):
    documents = MultipleFileField(
        validators=[
            MultiFileAllowed(['jpg', 'png', 'jpeg', 'tif', 'bmp', 'pdf'], message='Select a JPG, BMP, PNG, TIF or PDF file smaller than 10MB'),
            FileSizeLimit(10)
        ]
    )

    more_files = BooleanField('more_files')


class DeleteForm(FlaskForm):
    section = HiddenField(
        validators=[DataRequired(message='Field is required')]
    )

    file = HiddenField(
        validators=[DataRequired(message='Field is required')]
    )
