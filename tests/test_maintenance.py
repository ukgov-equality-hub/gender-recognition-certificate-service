import os
from unittest import mock
from grc import create_app
from grc.config import TestConfig

class MaintenanceConfig(TestConfig):
    MAINTENANCE_MODE = 'ON'


@mock.patch.dict(os.environ, {'MAINTENANCE_MODE': 'ON'})
def test_maintenance_mode():
    flask_app = create_app(MaintenanceConfig)
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()

    response = client.get('/')
    print(response, flush=True)
    assert response.status_code == 503
