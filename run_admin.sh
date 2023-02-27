#!/bin/bash

#flask run --host=0.0.0.0 --port=3001
waitress-serve --call --port=3001 'admin:create_app'