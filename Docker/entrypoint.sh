#!/bin/bash

set -e

prod_startup() {

    printf " \n"
    # Run database migrations
    echo "<<<<<<<<<<<<<<<<<<<< Waiting for postgres... >>>>>>>>>>>>>>>>>>>>>>>>"
    while ! nc -z rbac_database 5432; do
        sleep 2
    done
    echo "<<<<<<<<<<<<<<<<<<<< PostgreSQL started >>>>>>>>>>>>>>>>>>>>>>>>"
    flask db upgrade

    printf " \n"
    echo "<<<<<<<<<<<<<<<<<<<< Start Supervisor >>>>>>>>>>>>>>>>>>>>>>>>"
    supervisord -c /usr/local/etc/supervisord.conf
}

prod_startup
