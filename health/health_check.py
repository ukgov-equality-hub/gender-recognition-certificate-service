from healthcheck import HealthCheck


class HealthCheckBase:

    def __init__(self):
        self.health = HealthCheck()
        self.health.add_check(self.check)

    @staticmethod
    def check():
        return True, 200
