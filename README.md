# FDGRM.

![main workflow](https://github.com/vargg/foodgram-project-react/actions/workflows/fdgrm_workflow.yaml/badge.svg)

http://84.201.173.122/

## Стэк
[Python](https://www.python.org/) v.3.9, [Django](https://www.djangoproject.com/) v.3.2.7, [Django REST framework](https://www.django-rest-framework.org/) v.3.12.4, [django filter](https://django-filter.readthedocs.io/en/stable/) v.2.4.0, [nginx](https://nginx.org/en/docs/) v.1.20.1, [PostgreSQL](https://www.postgresql.org) v.13.4, [Docker](https://www.docker.com/) v.20.10.8.

## Описание.
Сервис для публикации рецептов. Реализована возможность подписки на других пользователей, добавление рецептов в избранное, а так же в список для покупок с возможностью получения общего списка ингредиентов.

## API.
Помимо веб-интерфейса, имеется доступ через API. Подробная информация по работе с API доступна на странице `api/docs/`.

### Пример запроса:
- получение токена по email и паролю

request `api/auth/token/login/ [POST]`
```json
{
  "email": "str",
  "password": "str"
}
```
response
```json
{
  "auth_token": "str"
}
```

## Установка и запуск.
Для запуска требуются [docker](https://docs.docker.com/get-docker/) и [docker compose](https://docs.docker.com/compose/install/).
Клонировать репозиторий:
```shell
git clone https://github.com/vargg/yamdb_final.git
```
В корневом каталоге проекта создать файл `.env` в котором должны быть заданы следующие переменные:
```
-DB_NAME
-DB_ENGINE
-DB_USER
-DB_PASSWORD
-POSTGRES_PASSWORD
-DB_HOST
-DB_PORT
-DEBUG
-DJANGO_SECRET_KEY
```
Запуск контейнеров:
```shell
docker-compose up
```
Сервис будет доступен по ссылке [http://localhost](http://localhost).

Создание и применение миграций:
```shell
docker-compose exec -T backend python manage.py makemigrations
docker-compose exec -T backend python manage.py migrate
```
Для сбора статики:
```shell
docker-compose exec -T backend python manage.py collectstatic --no-input
```
Загрузка в базу данных фикстур (тэги и список ингредиентов):
```shell
docker-compose exec -T backend python manage.py loaddata fixtures.json
```
Остановка:
```shell
docker-compose down
```
