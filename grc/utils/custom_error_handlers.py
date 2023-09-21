from flask import Flask, render_template
import sentry_sdk
from sentry_sdk import capture_exception


class CustomErrorHandlers:
    def __init__(self, app: Flask):
        app.register_error_handler(404, self.error_404)
        app.register_error_handler(429, self.error_429)
        app.register_error_handler(503, self.error_503)
        app.register_error_handler(Exception, self.error_default)

        sentry_sdk.init(
            dsn=app.config['SENTRY_URL'],

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0
        )

    @staticmethod
    def error_404(e):
        print(f"error 404: {e}", flush=True)
        capture_exception(e)
        return render_template('custom-error-templates/404.html'), 404

    @staticmethod
    def error_429(e):
        print(f"error 429: {e}", flush=True)
        capture_exception(e)
        return render_template('custom-error-templates/429.html')

    @staticmethod
    def error_503(e):
        print(f"error 503: {e}", flush=True)
        capture_exception(e)
        return render_template('custom-error-templates/503.html'), 503

    @staticmethod
    def error_default(e):
        print(f"error default: {e}", flush=True)
        capture_exception(e)
        return render_template('custom-error-templates/error-default.html'), 500
