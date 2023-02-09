#!/bin/bash

echo "In run.sh...."

export FLASK_APP=grc
export FLASK_ENV=production
export FLASK_DEBUG=1

flask db init
flask db migrate
flask db upgrade

flask run --host=0.0.0.0

#while true
#do
#  sleep 30
#done