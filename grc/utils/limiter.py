from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def limiter(app):

    if not app.config['MEMORY_STORAGE_URL']:
        return None

    return Limiter(
        get_remote_address,
        app=app,
        meta_limits=["5 per minute"],
        default_limits=["200 per day", "50 per hour"],
        storage_uri=app.config['MEMORY_STORAGE_URL'],
        strategy="fixed-window"
    )
