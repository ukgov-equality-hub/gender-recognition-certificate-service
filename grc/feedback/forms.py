from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    how_easy_to_complete_application = RadioField(
        choices=[
            ('1_VERY_EASY', 'Very easy'),
            ('2_EASY', 'Easy'),
            ('3_NEUTRAL', 'Neither easy nor difficult'),
            ('4_DIFFICULT', 'Difficult'),
            ('5_VERY_DIFFICULT', 'Very difficult'),
            ('6_COULD_NOT_COMPLETE', "I couldn't complete  my application")
        ],
        validators=[DataRequired(message='Select how easy it was to complete your application')]
    )

    any_questions_difficult_to_answer = RadioField(
        choices=[
            ('YES', 'Yes'),
            ('NO', 'No')
        ],
        validators=[DataRequired(message='Select if you found any of the questions difficult to answer')]
    )

    which_questions_difficult_to_answer = StringField()

    needed_to_call_admin_team = RadioField(
        choices=[
            ('YES', 'Yes'),
            ('NO', 'No')
        ],
        validators=[DataRequired(message='Select if you needed to call the admin team for help with your application')]
    )

    what_did_you_need_help_with = StringField()

    used_doc_checker = RadioField(
        choices=[
            ('YES', 'Yes'),
            ('NO', 'No'),
            ('DO_NOT_KNOW', "Don't know")
        ],
        validators=[DataRequired(message='Select if you used the tool to check which documents you needed to submit with your application')]
    )

    experience_of_using_doc_checker = StringField()

    any_other_suggestions = StringField()
