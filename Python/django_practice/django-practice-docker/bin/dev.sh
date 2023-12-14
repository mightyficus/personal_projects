#!/usr/bin/env bash
# bin/dev
# environment variables to be defined externally for security
# - MYSQL_USER
# - MYSQL_PASSWORD
# - MYSQL_ROOT_PASSWORD
DOMAIN=myproject.local

DJANGO_USE_DEBUG=1 \
DJANGO_USE_DEBUG_TOOLBAR=1 \
SITE_HOST="$DOMAIN" \
MEDIA_HOST="media.$DOMAIN" \
STATIC_HOST="static.$DOMAIN" \
MYSQL_HOST="localhost" \
MYSQL_DATABASE="myproject_db" \
    docker-compose $*