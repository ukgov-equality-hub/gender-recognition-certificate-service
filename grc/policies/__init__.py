from flask import Blueprint, render_template

policies = Blueprint('policies', __name__)


@policies.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    return render_template('policies/privacy-policy.html')
