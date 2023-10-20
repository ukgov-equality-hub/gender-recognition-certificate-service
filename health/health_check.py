from flask import Flask, jsonify
from healthcheck import HealthCheck


class HealthCheckBase:

    def __init__(self, app: Flask, flask_app: str):
        self.app = app
        self.flask_app = flask_app
        self.health = HealthCheck()
        self.health.add_check(self.check)
        self.url = '/health'
        self.endpoint = 'health'

    def add_rule(self):
        self.app.add_url_rule("/health", "health", view_func=lambda: self.health.run())

    @staticmethod
    def check():
        return True, 200
