from flask_wtf import Form, FlaskForm
from wtforms import MultipleFileField, HiddenField, RadioField, PasswordField, SubmitField, FormField, FieldList
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
                                 testValidator,
                                 MultiFileAllowed(['jpg', 'jpeg', 'png', 'tif', 'tiff', 'bmp', 'pdf'],
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


class PasswordForm(Form):
    aws_file_name = HiddenField(
        validators=[DataRequired(message='Field is required')]
    )

    original_file_name = HiddenField(
        validators=[DataRequired(message='Field is required')]
    )

    file_index = HiddenField(
        validators=[DataRequired(message='Field is required')]
    )

    password = PasswordField(
        # We would normally validate DataRequired
        # But we want to generate the error messages dynamically, including the file name in the error message
        # So we do this in the upload/__init__.py file
    )

    button_clicked = SubmitField()


class PasswordsForm(FlaskForm):
    files = FieldList(FormField(PasswordForm), min_entries=1)

    def get_csrf_token(self):
        return self._csrf.generate_csrf_token('csrf_token')


class DeleteAllFilesInSectionForm(FlaskForm):
    def get_csrf_token(self):
        return self._csrf.generate_csrf_token('csrf_token')
