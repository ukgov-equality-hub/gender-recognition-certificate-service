#!/bin/bash

flask db init
flask db migrate
flask db upgrade

waitress-serve --call 'dashboard:create_app'