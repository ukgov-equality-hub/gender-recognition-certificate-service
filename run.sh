#!/bin/bash

export FLASK_APP=grc/__init__.py
flask db init
flask db migrate
flask db upgrade

flask run --host=0.0.0.0