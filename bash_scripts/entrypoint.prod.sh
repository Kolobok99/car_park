#!/bin/bash

if [ "$SQL_DATABASE" = "mysql" ]
then
  echo "Waiting for mysql"

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "MySQL started!"

fi


exec "$@"

chmod +x app/entrypoint.sh

