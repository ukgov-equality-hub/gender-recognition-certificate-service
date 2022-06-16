from datetime import datetime
from dateutil import tz
import jinja2
import flask
from grc.external_services.aws_s3_client import AwsS3Client

blueprint = flask.Blueprint('filters', __name__)


@jinja2.pass_context
@blueprint.app_template_filter('format_date')
def format_date_filter(context, dt):
    if dt:
        dt = dt.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/London'))
        return datetime.strftime(dt, '%d/%m/%Y %H:%M')
    return ''

@jinja2.pass_context
@blueprint.app_template_filter('image_data')
def image_data_filter(context, image_name):
    print('image_data_filter', flush=True)
    print(image_name, flush=True)
    if image_name:
        data, width, height = AwsS3Client().download_object_data(image_name)
        return data
    return ''

@jinja2.pass_context
@blueprint.app_template_filter('image_width')
def image_width_filter(context, image_name):
    if image_name:
        data, width, height = AwsS3Client().download_object_data(image_name)
        width, height = check_image_sizes(width, height)

        return width
    return ''

@jinja2.pass_context
@blueprint.app_template_filter('image_height')
def image_height_filter(context, image_name):
    if image_name:
        data, width, height = AwsS3Client().download_object_data(image_name)
        width, height = check_image_sizes(width, height)

        return height
    return ''

def check_image_sizes(width, height):

    # Check sizes...595 x 842 pt
    ratio = 1.
    if width > 580:
        ratio = 580 / width
    elif height > 800:
        ratio = 800 / height
    width *= ratio
    height *= ratio
    return int(width), int(height)
