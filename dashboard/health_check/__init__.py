from flask import Blueprint
from health.health_check import HealthCheckBase

health_check = Blueprint('health_check', __name__)


@health_check.route('/health', methods=['GET'])
def index():
    check = HealthCheckBase()
    return check.health.run()