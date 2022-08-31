from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired


class UnlockFileForm(FlaskForm):
    file = FileField(
        validators=[
            DataRequired(message='Select a file to upload')
        ]
    )
