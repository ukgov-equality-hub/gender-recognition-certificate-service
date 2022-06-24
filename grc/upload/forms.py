from flask_wtf import FlaskForm
from wtforms import MultipleFileField, HiddenField, RadioField
from wtforms.validators import DataRequired
from grc.utils.form_custom_validators import MultiFileAllowed, fileSizeLimit, fileVirusScan, StrictRequiredIf


class UploadForm(FlaskForm):
    button_clicked = RadioField(
        choices=[
            ('Upload file', 'Upload file'),
            ('Save and continue', 'Save and continue')
        ],
        validators=[DataRequired(message="Click on either the 'Upload file' button or 'Save and continue' button")]
    )

    documents = MultipleFileField(
        validators=[
            StrictRequiredIf('button_clicked', 'Upload file',
                             message='Select a JPG, BMP, PNG, TIF or PDF file smaller than 10MB',
                             validators=[
                                 MultiFileAllowed(['jpg', 'png', 'jpeg', 'tif', 'bmp', 'pdf'],
                                                  message='Select a JPG, BMP, PNG, TIF or PDF file smaller than 10MB'),
                                 fileSizeLimit(10),
                                 fileVirusScan
                             ]),
        ]
    )

    def get_csrf_token(self):
        return self._csrf.generate_csrf_token('csrf_token')


class DeleteForm(FlaskForm):
    file = HiddenField(
        validators=[DataRequired(message='Field is required')]
    )

    def get_csrf_token(self):
        return self._csrf.generate_csrf_token('csrf_token')
