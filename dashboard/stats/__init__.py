import math
from datetime import date
import csv
from io import StringIO
from dateutil.relativedelta import relativedelta
from flask import Blueprint, render_template, request, make_response
from dashboard.stats.forms import DateRangeForm
from grc.models import db

stats = Blueprint('stats', __name__)


# QUESTIONS:
# SHOULD WE INCLUDE DELETED (I.E. APPLICATIONS REMOVED BY ADMIN)
# DATE RANGE CREATED, UPDATED OR BOTH?


def get_stats(stat, start_date=None, end_date=None, num_bands=8, download=False):
    if start_date and end_date:
        date_range = {
            "start_date": start_date, #if start_date < end_date else end_date,
            "end_date": end_date, #if end_date < start_date else start_date,
        }

    if stat == 'date_bands':
        if start_date and end_date:
            sql = """SELECT MAX(EXTRACT(DAY FROM updated - created)) AS diff
                    FROM application
                    WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'))
                        AND ((created >= :start_date AND created <= :end_date) OR (updated >= :start_date AND updated <= :end_date));"""
            result = db.session.execute(sql, date_range)
        else:
            sql = """SELECT MAX(EXTRACT(DAY FROM updated - created)) AS diff
                    FROM application
                    WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'));"""
            result = db.session.execute(sql)

        diff = result.mappings().first()
        diff = int(diff['diff']) if diff['diff'] else 0
        if diff < num_bands: diff = num_bands + 1
        return math.ceil(diff / num_bands)

    elif stat == 'applications_by_status':
        if start_date and end_date:
            sql = """SELECT status AS "application status", COUNT(*) AS "number of applications"
                    FROM application
                    WHERE (created >= :start_date AND created <= :end_date) OR (updated >= :start_date AND updated <= :end_date)
                    GROUP BY status;"""
            result = db.session.execute(sql, date_range)
        else:
            sql = """SELECT status AS "application status", COUNT(*) AS "number of applications"
                    FROM application
                    GROUP BY status;"""
            result = db.session.execute(sql)

        return \
            ['application status', 'number of applications'], \
            result.mappings().all()

    elif stat == 'started_applications_by_month':
        if start_date and end_date:
            sql = """SELECT date AS "application date", num AS "number of applications"
                FROM (
                    SELECT COUNT(*) AS num, SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4) AS date, CAST(TO_CHAR(updated, 'YYYYMM') AS INTEGER) AS order_value
                    FROM application
                    WHERE (status IN ('STARTED'))
                        AND ((created >= :start_date AND created <= :end_date) OR (updated >= :start_date AND updated <= :end_date))
                    GROUP BY SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4), TO_CHAR(updated, 'YYYYMM')
                ) AS t
                ORDER BY order_value;"""
            result = db.session.execute(sql, date_range)
        else:
            sql = """SELECT date AS "application date", num AS "number of applications"
                FROM (
                    SELECT COUNT(*) AS num, SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4) AS date, CAST(TO_CHAR(updated, 'YYYYMM') AS INTEGER) AS order_value
                    FROM application
                    WHERE (status IN ('STARTED'))
                    GROUP BY SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4), TO_CHAR(updated, 'YYYYMM')
                ) AS t
                ORDER BY order_value;"""
            result = db.session.execute(sql)

        return \
            ['application date', 'number of applications'], \
            result.mappings().all()

    elif stat == 'completed_applications_by_month':
        if start_date and end_date:
            sql = """SELECT date AS "application date", num AS "number of applications"
                FROM (
                    SELECT COUNT(*) AS num, SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4) AS date, CAST(TO_CHAR(updated, 'YYYYMM') AS INTEGER) AS order_value
                    FROM application
                    WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'))
                        AND ((created >= :start_date AND created <= :end_date) OR (updated >= :start_date AND updated <= :end_date))
                    GROUP BY SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4), TO_CHAR(updated, 'YYYYMM')
                ) AS t
                ORDER BY order_value;"""
            result = db.session.execute(sql, date_range)
        else:
            sql = """SELECT date AS "application date", num AS "number of applications"
                FROM (
                    SELECT COUNT(*) AS num, SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4) AS date, CAST(TO_CHAR(updated, 'YYYYMM') AS INTEGER) AS order_value
                    FROM application
                    WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'))
                    GROUP BY SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4), TO_CHAR(updated, 'YYYYMM')
                ) AS t
                ORDER BY order_value;"""
            result = db.session.execute(sql)

        return \
            ['application date', 'number of applications'], \
            result.mappings().all()

    elif stat == 'applications_by_month':
        if start_date and end_date:
            sql = """SELECT date AS "application date", num AS "number of applications", status
                    FROM (
                        SELECT date, num, 'started' AS status, order_value
                        FROM (
                            SELECT COUNT(*) AS num, SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4) AS date, CAST(TO_CHAR(updated, 'YYYYMM') AS INTEGER) AS order_value
                            FROM application
                            WHERE (status IN ('STARTED'))
                                AND ((created >= :start_date AND created <= :end_date) OR (updated >= :start_date AND updated <= :end_date))
                            GROUP BY SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4), TO_CHAR(updated, 'YYYYMM')
                        ) AS t
                        UNION
                        SELECT date, num, 'submitted' AS status, order_value
                        FROM (
                            SELECT COUNT(*) AS num, SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4) AS date, CAST(TO_CHAR(updated, 'YYYYMM') AS INTEGER) AS order_value
                            FROM application
                            WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'))
                                AND ((created >= :start_date AND created <= :end_date) OR (updated >= :start_date AND updated <= :end_date))
                            GROUP BY SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4), TO_CHAR(updated, 'YYYYMM')
                        ) AS t
                    ) AS t
                    ORDER BY order_value, status DESC;"""
            result = db.session.execute(sql, date_range)
        else:
            sql = """SELECT date AS "application date", num AS "number of applications", status
                    FROM (
                        SELECT date, num, 'started' AS status, order_value
                        FROM (
                            SELECT COUNT(*) AS num, SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4) AS date, CAST(TO_CHAR(updated, 'YYYYMM') AS INTEGER) AS order_value
                            FROM application
                            WHERE (status IN ('STARTED'))
                            GROUP BY SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4), TO_CHAR(updated, 'YYYYMM')
                        ) AS t
                        UNION
                        SELECT date, num, 'submitted' AS status, order_value
                        FROM (
                            SELECT COUNT(*) AS num, SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4) AS date, CAST(TO_CHAR(updated, 'YYYYMM') AS INTEGER) AS order_value
                            FROM application
                            WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'))
                            GROUP BY SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4), TO_CHAR(updated, 'YYYYMM')
                        ) AS t
                    ) AS t
                    ORDER BY order_value, status DESC;"""
            result = db.session.execute(sql)

        return \
            ['application date', 'number of applications', 'status'], \
            result.mappings().all()

    elif stat == 'applications_by_month_joined':
        sql = """SELECT t1.application_date AS "application date",
                    t1.started AS "number of applications started",
                    t2.submitted AS "number of applications submitted"
                FROM (
                    SELECT date AS application_date, num AS started
                    FROM (
                        SELECT COUNT(*) AS num, SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4) AS date, CAST(TO_CHAR(updated, 'YYYYMM') AS INTEGER) AS order_value
                        FROM application
                        WHERE (status IN ('STARTED'))
                        GROUP BY SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4), TO_CHAR(updated, 'YYYYMM')
                    ) AS t
                    ORDER BY order_value) AS t1
                INNER JOIN (
                    SELECT date AS application_date, num AS submitted
                    FROM (
                        SELECT COUNT(*) AS num, SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4) AS date, CAST(TO_CHAR(updated, 'YYYYMM') AS INTEGER) AS order_value
                        FROM application
                        WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'))
                        GROUP BY SUBSTRING(TO_CHAR(updated, 'Month'), 1, 3) || '-' || SUBSTRING(TO_CHAR(updated, 'YYYY'), 3, 4), TO_CHAR(updated, 'YYYYMM')
                    ) AS t
                    ORDER BY order_value) AS t2 ON t1.application_date = t2.application_date;"""
        result = db.session.execute(sql)

        return \
            ['application date', 'number of applications', 'status'], \
            result.mappings().all()

    elif stat == 'days_to_complete_application':
        if start_date and end_date:
            sql = """SELECT diff AS "number of days", COUNT(*) AS "number of applications"
                    FROM (
                        SELECT EXTRACT(DAY FROM updated - created) + 1 AS diff
                        FROM application
                        WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'))
                            AND ((created >= :start_date AND created <= :end_date) OR (updated >= :start_date AND updated <= :end_date))
                    ) AS t
                    GROUP BY diff
                    ORDER BY diff;"""
            result = db.session.execute(sql, date_range)
        else:
            sql = """SELECT diff AS "number of days", COUNT(*) AS "number of applications"
                    FROM (
                        SELECT EXTRACT(DAY FROM updated - created) + 1 AS diff
                        FROM application
                        WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'))
                    ) AS t
                    GROUP BY diff
                    ORDER BY diff;"""
            result = db.session.execute(sql)

        return \
            ['number of days', 'number of applications'], \
            result.mappings().all()

    elif stat == 'days_to_complete_application_banded':
        band_value = get_stats('date_bands', start_date=start_date, end_date=end_date, num_bands=num_bands, download=download)
        _, data = get_stats('days_to_complete_application', start_date=start_date, end_date=end_date, num_bands=num_bands, download=download)

        results = []
        for i in range(1, num_bands + 1):
            applications = [x['number of applications'] for x in data if x['number of days'] > (band_value * (i - 1)) if x['number of days'] <= (band_value * i)]
            results.append({ 'band': i, 'range': f'{(band_value * (i - 1) + 1)}-{(band_value * i)}', 'number of applications': sum(applications) })

        return \
            ['band', 'range', 'number of applications'], \
            results

    elif stat == 'sessions_to_complete_application':
        if start_date and end_date:
            sql = """SELECT COUNT(*) AS "number of applications", COALESCE(number_sessions, 1) AS "number of sessions"
                    FROM application
                    WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'))
                        AND ((created >= :start_date AND created <= :end_date) OR (updated >= :start_date AND updated <= :end_date))
                    GROUP BY number_sessions
                    ORDER BY number_sessions;"""
            result = db.session.execute(sql, date_range)
        else:
            sql = """SELECT COUNT(*) AS "number of applications", COALESCE(number_sessions, 1) AS "number of sessions"
                    FROM application
                    WHERE (status IN ('COMPLETED', 'SUBMITTED', 'DOWNLOADED'))
                    GROUP BY number_sessions
                    ORDER BY number_sessions;"""
            result = db.session.execute(sql)

        return \
            ['number of applications', 'number of sessions'], \
            result.mappings().all()

    elif stat == 'sessions_to_complete_application_banded':
        band_value = get_stats('date_bands', start_date=start_date, end_date=end_date, num_bands=num_bands, download=download)
        _, data = get_stats('sessions_to_complete_application', start_date=start_date, end_date=end_date, num_bands=num_bands, download=download)

        results = []
        for i in range(1, num_bands + 1):
            applications = [x['number of applications'] for x in data if x['number of sessions'] > (band_value * (i - 1)) if x['number of sessions'] <= (band_value * i)]
            results.append({ 'band': i, 'range': f'{(band_value * (i - 1) + 1)}-{(band_value * i)}', 'number of applications': sum(applications) })

        return \
            ['band', 'range', 'number of applications'], \
            results

    elif stat == 'number_of_duplicate_emailaddresses':
        if start_date and end_date:
            sql = """SELECT COUNT(*) AS "number of applications"
                    FROM (
                        SELECT COUNT(*) AS num
                        FROM application
                        WHERE ((created >= :start_date AND created <= :end_date) OR (updated >= :start_date AND updated <= :end_date))
                        GROUP BY email
                    ) AS t
                    WHERE (num > 1);"""
            result = db.session.execute(sql, date_range)
        else:
            sql = """SELECT COUNT(*) AS "number of applications"
                    FROM (
                        SELECT COUNT(*) AS num
                        FROM application
                        GROUP BY email
                    ) AS t
                    WHERE (num > 1);"""
            result = db.session.execute(sql)

        return \
            ['number of applications'], \
            result.mappings().all()

    elif stat == 'duplicate_emailaddresses':
        if start_date and end_date:
            sql = """SELECT num AS "number of applications", COUNT(*) AS "number of users"
            FROM (
                SELECT COUNT(*) AS num
                FROM application
                WHERE ((created >= :start_date AND created <= :end_date) OR (updated >= :start_date AND updated <= :end_date))
                GROUP BY email
            ) AS t
            GROUP BY num
            ORDER BY num;"""
            result = db.session.execute(sql, date_range)
        else:
            sql = """SELECT num AS "number of applications", COUNT(*) AS "number of users"
            FROM (
                SELECT COUNT(*) AS num
                FROM application
                GROUP BY email
            ) AS t
            GROUP BY num
            ORDER BY num;"""
            result = db.session.execute(sql)

        return \
            ['number of applications', 'number of users'], \
            result.mappings().all()

    return None, None


def get_daterange(form=None):
    start_date = request.args.get('start_date', default=None)
    end_date = request.args.get('end_date', default=None)
    date_range = request.args.get('date_range', default=None)

    if form:
        try:
            start_date = date(int(form.start_date_year.data), int(form.start_date_month.data), int(form.start_date_day.data))
            end_date = date(int(form.end_date_year.data), int(form.end_date_month.data), int(form.end_date_day.data))
            date_range = 'custom'
        except:
            pass
    elif start_date and end_date:
        try:
            start_date = date(start_date)
            end_date = date(end_date)
        except:
            pass
    else:
        if date_range == 'last_30_days':
            end_date = date.today()
            start_date = end_date - relativedelta(days=30)
        elif date_range == 'last_3_months':
            end_date = date.today()
            start_date = end_date - relativedelta(months=3)
        elif date_range == 'last_6_months':
            end_date = date.today()
            start_date = end_date - relativedelta(months=6)
        elif date_range == 'last_12_months':
            end_date = date.today()
            start_date = end_date - relativedelta(months=12)
        elif date_range == 'all_time':
            end_date = date.today()
            start_date = end_date - relativedelta(years=10)

    return start_date, end_date, date_range


@stats.route('/', methods=['GET', 'POST'])
def index():
    form = DateRangeForm()

    message = ""
    start_date = None
    end_date = None
    date_range = None

    if request.method == 'POST':
        if form.validate_on_submit():
            start_date, end_date, date_range = get_daterange(form)
    else:
        start_date, end_date, date_range = get_daterange()

    stats = dict()
    all_measures = [
        'number_of_duplicate_emailaddresses',
        'applications_by_status',
        'applications_by_month',
        #'started_applications_by_month',
        #'completed_applications_by_month',
        'days_to_complete_application_banded',
        'sessions_to_complete_application_banded',
    ]

    for measure in all_measures:
        _, data = get_stats(measure, start_date=start_date, end_date=end_date)
        stats[measure] = data

    #applications_in_progress = sum([x['number of applications'] for x in stats['started_applications_by_month']])
    applications_in_progress = 0
    applications_started = 0
    applications_submitted = 0
    try:
        applications_in_progress = [x['number of applications'] for x in stats['applications_by_status'] if x['application status'] == 'STARTED'][0]
        applications_started = sum([x['number of applications'] for x in stats['applications_by_status']])
        applications_submitted = sum([x['number of applications'] for x in stats['applications_by_status'] if x['application status'] in ['COMPLETED', 'SUBMITTED', 'DOWNLOADED']])
    except:
        pass

    stats['applications_in_progress'] = applications_in_progress
    stats['total_applications_started'] = applications_started
    stats['total_applications_submitted'] = applications_submitted
    if applications_started > 0 and applications_submitted > 0:
        stats['total_applications_submitted_percent'] = int(float(applications_submitted) / float(applications_started) * 100)

    return render_template(
        'stats/stats.html',
        form=form,
        message=message,
        date_range=date_range,
        start_date=start_date,
        end_date=end_date,
        stats=stats
    )


@stats.route('/download/<stat>', methods=['GET'])
def download(stat):
    start_date, end_date, _ = get_daterange()
    fieldnames, data = get_stats(stat, start_date=start_date, end_date=end_date, download=True)

    csv_stream = StringIO()
    writer = csv.DictWriter(csv_stream, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

    csv_stream.seek(0)
    csv_bytes = csv_stream.read()

    response = make_response(csv_bytes)
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename=f'{stat}.csv')
    return response
