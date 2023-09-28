import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def limiter(app):
    print(f'MEMORY_STORAGE_URL OS = {os.environ.get("MEMORY_STORAGE_URL")}')
    print(f'MEMORY_STORAGE_URL APP = {app.config["MEMORY_STORAGE_URL"]}')
    if not app.config['MEMORY_STORAGE_URL']:
        return None
    storage_uri = app.config['MEMORY_STORAGE_URL'].replace('rediss://', 'redis+cluster://dummy_user')
    print(f'storage_uri = {storage_uri}', flush=True)
    return Limiter(
        get_remote_address,
        app=app,
        meta_limits=["5 per minute"],
        default_limits=["200 per day", "50 per hour"],
        storage_uri=storage_uri
    )
