import datetime
from admin.jobs import calculate_earliest_allowed_inactive_application_updated_date, calculate_last_updated_date, calculate_earliest_allowed_security_code_creation_time


days_between_last_update_and_deletion = 183  # approximately 6 months
hours_between_security_code_creation_and_expiry = 24


def test_calculate_earliest_allowed_inactive_application_updated_date():
    check_calculate_earliest_allowed_inactive_application_updated_date(now='2022-08-11 16:57:02', expected='2022-02-09 16:57:02')
    check_calculate_earliest_allowed_inactive_application_updated_date(now='2022-08-11 00:23:07', expected='2022-02-09 00:23:07')
    check_calculate_earliest_allowed_inactive_application_updated_date(now='2022-01-24 00:23:07', expected='2021-07-25 00:23:07')


def check_calculate_earliest_allowed_inactive_application_updated_date(now, expected):
    now_dt = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

    earliest_allowed_inactive_application_updated_date = calculate_earliest_allowed_inactive_application_updated_date(now_dt, days_between_last_update_and_deletion)

    expected_earliest_allowed_inactive_application_updated_date = datetime.datetime.strptime(expected, '%Y-%m-%d %H:%M:%S')
    assert earliest_allowed_inactive_application_updated_date == expected_earliest_allowed_inactive_application_updated_date


def test_calculate_last_updated_date():
    check_calculate_last_updated_date(today='2022-08-11', days_before_deletion=7, expected_last_updated='2022-02-16')
    check_calculate_last_updated_date(today='2022-08-11', days_before_deletion=30, expected_last_updated='2022-03-11')
    check_calculate_last_updated_date(today='2022-08-11', days_before_deletion=90, expected_last_updated='2022-05-10')


def check_calculate_last_updated_date(today, days_before_deletion, expected_last_updated):
    today_dt = datetime.datetime.strptime(today, '%Y-%m-%d')

    last_updated_date = calculate_last_updated_date(today_dt, days_before_deletion, days_between_last_update_and_deletion)

    expected_last_updated_dt = datetime.datetime.strptime(expected_last_updated, '%Y-%m-%d')
    assert last_updated_date == expected_last_updated_dt


def test_calculate_earliest_allowed_security_code_creation_time():
    check_calculate_earliest_allowed_security_code_creation_time(now='2022-08-11 16:57:02', expected_earliest_last_updated='2022-08-10 16:57:02')
    check_calculate_earliest_allowed_security_code_creation_time(now='2022-08-11 00:23:07', expected_earliest_last_updated='2022-08-10 00:23:07')
    check_calculate_earliest_allowed_security_code_creation_time(now='2022-01-01 12:34:56', expected_earliest_last_updated='2021-12-31 12:34:56')


def check_calculate_earliest_allowed_security_code_creation_time(now, expected_earliest_last_updated):
    now_dt = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

    earliest_allowed_inactive_application_updated_date = calculate_earliest_allowed_security_code_creation_time(now_dt, hours_between_security_code_creation_and_expiry)

    expected_earliest_allowed_inactive_application_updated_date = datetime.datetime.strptime(expected_earliest_last_updated, '%Y-%m-%d %H:%M:%S')
    assert earliest_allowed_inactive_application_updated_date == expected_earliest_allowed_inactive_application_updated_date
