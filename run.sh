#!/bin/bash

echo "DATABASE_URL is <${DATABASE_URL}>"
echo "FLASK_APP is >${FLASK_APP}>"

export FLASK_ENV=production
export FLASK_DEBUG=1

flask db init
flask db migrate
flask db upgrade

flask run --host=0.0.0.0