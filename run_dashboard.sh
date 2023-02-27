#!/bin/bash

#flask run --host=0.0.0.0 --port=3002
waitress-serve --call --port=3002 'dashboard:create_app'