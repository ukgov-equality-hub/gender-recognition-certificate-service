#!/bin/bash

echo "DATABASE_URL is <${DATABASE_URL}>"
echo "FLASK_APP is >${FLASK_APP}>"

#flask db init
#flask db migrate
#flask db upgrade

flask run --host=0.0.0.0