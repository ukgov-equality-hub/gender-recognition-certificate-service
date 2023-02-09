#!/bin/bash

echo "In run.sh...."

export FLASK_APP=grc
flask db init
flask db migrate
flask db upgrade

flask run --host=0.0.0.0

#while true
#do
#  sleep 30
#done