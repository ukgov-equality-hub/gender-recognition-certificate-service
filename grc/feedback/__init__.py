from flask import Blueprint, render_template, url_for

from grc.external_services.gov_uk_notify import GovUkNotify
from grc.models import db, Feedback
from grc.feedback.forms import FeedbackForm
from grc.utils.redirect import local_redirect

feedback = Blueprint('feedback', __name__)


@feedback.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback_db_row = Feedback(
            how_easy_to_complete_application = form.how_easy_to_complete_application.data,
            any_questions_difficult_to_answer = form.any_questions_difficult_to_answer.data,
            which_questions_difficult_to_answer = form.which_questions_difficult_to_answer.data,
            needed_to_call_admin_team = form.needed_to_call_admin_team.data,
            what_did_you_need_help_with = form.what_did_you_need_help_with.data,
            used_doc_checker = form.used_doc_checker.data,
            experience_of_using_doc_checker = form.experience_of_using_doc_checker.data,
            any_other_suggestions = form.any_other_suggestions.data
        )
        db.session.add(feedback_db_row)
        db.session.commit()

        GovUkNotify().send_email_feedback(
            how_easy_to_complete_application = form.how_easy_to_complete_application.data,
            any_questions_difficult_to_answer = form.any_questions_difficult_to_answer.data,
            which_questions_difficult_to_answer = form.which_questions_difficult_to_answer.data,
            needed_to_call_admin_team = form.needed_to_call_admin_team.data,
            what_did_you_need_help_with = form.what_did_you_need_help_with.data,
            used_doc_checker = form.used_doc_checker.data,
            experience_of_using_doc_checker = form.experience_of_using_doc_checker.data,
            any_other_suggestions = form.any_other_suggestions.data
        )

        return local_redirect(url_for('feedback.feedback_received'))

    return render_template(
        'feedback/feedback-form.html',
        form=form
    )


@feedback.route('/feedback-received', methods=['GET', 'POST'])
def feedback_received():
    return render_template('feedback/feedback-received.html')
