import csv
from io import StringIO
from flask import Blueprint, render_template, make_response
from dashboard.feedback.feedback_viewmodel import FeedbackViewModel
from grc.models import Feedback

feedback = Blueprint('feedback', __name__)


@feedback.route('/feedback', methods=['GET'])
def view_feedback():
    feedback_db_rows = Feedback.query.order_by(Feedback.created.desc())
    feedback_objects = [FeedbackViewModel(feedback_db_row) for feedback_db_row in feedback_db_rows]

    return render_template(
        'feedback/view-feedback.html',
        all_feedback=feedback_objects,
        num_feedback=len(feedback_objects)
    )


@feedback.route('/feedback/download', methods=['GET'])
def download_feedback():
    feedback_db_rows = Feedback.query.order_by(Feedback.created.desc())
    feedback_dictionaries = [vars(FeedbackViewModel(feedback_db_row)) for feedback_db_row in feedback_db_rows]
    fieldnames = [
        'id',
        'created',
        'how_easy_to_complete_application',
        'any_questions_difficult_to_answer',
        'which_questions_difficult_to_answer',
        'needed_to_call_admin_team',
        'what_did_you_need_help_with',
        'used_doc_checker',
        'experience_of_using_doc_checker',
        'any_other_suggestions'
    ]

    csv_stream = StringIO()
    writer = csv.DictWriter(csv_stream, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(feedback_dictionaries)

    csv_stream.seek(0)
    csv_bytes = csv_stream.read()

    response = make_response(csv_bytes)
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='feedback.csv')
    return response
