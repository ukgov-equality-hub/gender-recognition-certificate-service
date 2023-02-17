from datetime import datetime
from dateutil import tz
import jinja2
import flask
from wtforms import FieldList
from grc.models import ApplicationStatus

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
@blueprint.app_template_filter('application_status')
def application_status_filter(context, status):
    if status == ApplicationStatus.COMPLETED:
        return 'COMPLETED'
    elif status == ApplicationStatus.DELETED:
        return 'DELETED'
    elif status == ApplicationStatus.STARTED:
        return 'STARTED'
    elif status == ApplicationStatus.SUBMITTED:
        return 'SUBMITTED'
    elif status == ApplicationStatus.DOWNLOADED:
        return 'DOWNLOADED'
    elif status == ApplicationStatus.ABANDONED:
        return 'ABANDONED'


@jinja2.pass_context
@blueprint.app_template_filter('remove_file_name_from_error')
def remove_file_name_from_error_filter(context, error):
    try:
        if error.index(':'):
            return error[error.index(':') + 1:].strip()
    except:
        pass
    return error


@jinja2.pass_context
@blueprint.app_template_filter('plural_text')
def plural_text_filter(context, data):
    try:
        if data[1] != 1:
            if data[0] == 'address': return 'addresses'
            return f'{data[0]}s'
    except:
        pass
    return data[0]


@jinja2.pass_context
@blueprint.app_template_filter('number_with_commas')
def number_with_commas_filter(context, num):
    try:
        return f'{num:,}'
    except:
        pass
    return num


@jinja2.pass_context
@blueprint.app_template_filter('is_FieldList')
def is_FieldList(context, value):
    return isinstance(value, FieldList)


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
