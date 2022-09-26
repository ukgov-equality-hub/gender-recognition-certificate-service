from flask import Blueprint, render_template
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
