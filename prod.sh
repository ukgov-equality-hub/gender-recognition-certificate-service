#!/bin/bash

flask db init
flask db migrate
flask db upgrade

newrelic-admin generate-config eu01xxb0184e80946179dc753dd2e8d569daNRAL newrelic.ini

NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program waitress-serve --call 'grc:create_app'