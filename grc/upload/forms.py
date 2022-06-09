from flask_wtf import FlaskForm
from wtforms import MultipleFileField, BooleanField, HiddenField
from wtforms.validators import DataRequired
from grc.utils.form_custom_validators import MultiFileAllowed, fileSizeLimit, fileVirusScan


class UploadForm(FlaskForm):
    documents = MultipleFileField(
        validators=[
            MultiFileAllowed(['jpg', 'png', 'jpeg', 'tif', 'bmp', 'pdf', 'txt'], message='Select a JPG, BMP, PNG, TIF or PDF file smaller than 10MB'),
            fileSizeLimit(10),
            fileVirusScan
        ]
    )

    more_files = BooleanField('more_files')

    def get_csrf_token(self):
        return self._csrf.generate_csrf_token('csrf_token')


class DeleteForm(FlaskForm):
    file = HiddenField(
        validators=[DataRequired(message='Field is required')]
    )

    def get_csrf_token(self):
        return self._csrf.generate_csrf_token('csrf_token')
