#!/bin/bash

echo "DATABASE_URL is <${DATABASE_URL}>"
echo "FLASK_APP is <${FLASK_APP}>"
echo "FLASK_ENV is <${FLASK_ENV}>"

echo "flask db commands commented out to bypass db migration"
#flask db init
#flask db migrate
#flask db upgrade

flask run --host=0.0.0.0 -p 3000