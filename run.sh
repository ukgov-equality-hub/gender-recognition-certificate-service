#!/bin/bash

echo "In run.sh...."
pwd
find . -name "*.py"

export FLASK_APP=grc:create_app
flask db init
flask db migrate
flask db upgrade

flask run --host=0.0.0.0