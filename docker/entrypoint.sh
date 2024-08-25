#!/usr/bin/env bash

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_DB_HOST 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_DB_HOST}/${POSTGRES_DB}"

cd /app || exit

# Install and build frontend
yarn install --frozen-lock-file --production=false

# Django Setup
python ./manage.py migrate --no-input
python ./manage.py compilemessages --ignore=.venv

if [ "$#" ] ; then
  exec "$@";
fi

if [ "$DEV_MODE" = "true" ] ; then
  # Start Dev server in dev mode
  exec bash /run-dev-servers.sh
else
  # Build and run production server
  yarn build
  python ./manage.py collectstatic --no-input
  exec granian --interface "${SERVER_INTERFACE:=wsgi}" recipe_repo.${SERVER_INTERFACE:=wsgi}:application --host 0.0.0.0 --port 8000
fi
