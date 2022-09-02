from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField
from wtforms.validators import DataRequired


class UnlockFileForm(FlaskForm):
    file = FileField(
        validators=[
            DataRequired(message='Select a file to upload')
        ]
    )

    pdf_password = PasswordField()
