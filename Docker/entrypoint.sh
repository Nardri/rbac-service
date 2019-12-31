#!/bin/bash

set -e

API_startup() {
    # Run database migrations

    dockerize -wait tcp://rbac_database:5432 -timeout 1m
#    dockerize -wait tcp://account_database:5432 -timeout 1m
    flask db upgrade

    # Start server
    echo -e "\n \n"
    gunicorn --access-logfile '-' \
        --workers 2 --timeout 3600 \
        manage:app --bind 0.0.0.0:5000 --reload \
        --access-logformat "%(h)s %(u)s %(t)s '%(r)s' %(s)s '%(f)s' '%(a)s'"
}

API_startup
