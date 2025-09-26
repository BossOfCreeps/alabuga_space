#!/bin/bash

# Ожидаем доступности базы данных
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

# Выполняем миграции
python manage.py migrate

# Собираем статику
python manage.py collectstatic --noinput

# Запускаем приложение
exec "$@"
