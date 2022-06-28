from flask import Blueprint


health_check = Blueprint('health_check', __name__)


@health_check.route('/health-check', methods=['GET'])
def index():
    return ('Health Check OK', 200)
