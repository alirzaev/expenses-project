#!/usr/bin/env sh

set -e

python manage.py migrate

if [ ! -f /data/initialized ]; then
  echo "from django.contrib.auth.models import User;" \
       "User.objects.create_superuser('$EXPENSES_USERNAME', '$EXPENSES_EMAIL', '$EXPENSES_PASSWORD')" \
       | python manage.py shell
  touch /data/initialized
fi

exec "$@"