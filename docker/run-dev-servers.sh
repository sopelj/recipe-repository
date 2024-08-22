#!/usr/bin/env bash
set -e

# Start Yarn Dev Server
yarn dev &

# Start Django Dev Server
python ./manage.py runserver_plus 0.0.0.0:8000 &

# Wait for exit
wait -n
exit $?
