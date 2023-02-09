#!/bin/bash

echo "In run.sh...." 1>&2

find . -name "*.py" 1>&2

export FLASK_APP=grc
flask db init
flask db migrate
flask db upgrade

flask run --host=0.0.0.0