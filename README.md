# команда для загрузки ингридиентов

python manage.py data_load

# команды для создания миграций после деплоя

docker-compose exec backend python manage.py migrate
docker-compose exec backend python python manage.py data_load
