from datetime import datetime
from wtforms import RadioField
from grc.feedback import FeedbackForm
from grc.models import Feedback


class FeedbackViewModel:
    id: int
    created: datetime
    how_easy_to_complete_application: str
    any_questions_difficult_to_answer: str
    which_questions_difficult_to_answer: str
    needed_to_call_admin_team: str
    what_did_you_need_help_with: str
    used_doc_checker: str
    experience_of_using_doc_checker: str
    any_other_suggestions: str

    def __init__(self, feedback: Feedback):
        self.id = feedback.id
        self.created = feedback.created
        self.how_easy_to_complete_application = feedback.how_easy_to_complete_application
        self.any_questions_difficult_to_answer = feedback.any_questions_difficult_to_answer
        self.which_questions_difficult_to_answer = feedback.which_questions_difficult_to_answer
        self.needed_to_call_admin_team = feedback.needed_to_call_admin_team
        self.what_did_you_need_help_with = feedback.what_did_you_need_help_with
        self.used_doc_checker = feedback.used_doc_checker
        self.experience_of_using_doc_checker = feedback.experience_of_using_doc_checker
        self.any_other_suggestions = feedback.any_other_suggestions

    @property
    def created_date_formatted(self) -> str:
        return self.created.strftime('%d %b %Y')

    @property
    def created_time_formatted(self) -> str:
        return self.created.strftime('%H:%M')

    @property
    def how_easy_to_complete_application_formatted(self) -> str:
        return get_form_choice_value(FeedbackForm().how_easy_to_complete_application, self.how_easy_to_complete_application)

    @property
    def any_questions_difficult_to_answer_formatted(self) -> str:
        return get_form_choice_value(FeedbackForm().any_questions_difficult_to_answer, self.any_questions_difficult_to_answer)

    @property
    def needed_to_call_admin_team_formatted(self) -> str:
        return get_form_choice_value(FeedbackForm().needed_to_call_admin_team, self.needed_to_call_admin_team)

    @property
    def used_doc_checker_formatted(self) -> str:
        return get_form_choice_value(FeedbackForm().used_doc_checker, self.used_doc_checker)


def get_form_choice_value(form_field: RadioField, value: str):
    for choice in form_field.choices:
        if choice[0] == value:
            return choice[1]
    return None
