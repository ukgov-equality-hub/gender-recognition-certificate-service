#!/bin/bash

flask db init
flask db migrate
flask db upgrade

waitress-serve --call 'grc:create_app'