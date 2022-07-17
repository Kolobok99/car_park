#!/bin/bash

if [ "$SQL_DATABASE" = "mysql" ]
then
  echo "Waiting for mysql"

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "MySQL started!"

fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"

chmod +x app/entrypoint.sh

