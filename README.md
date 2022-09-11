# Foodgram
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)

*Foodgram, «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.*


## Для работы с проектом локально необходимо выполнитье следующие действия:

1. Склонировать репозиторий
```
git clone git@github.com:kitah-ru/foodgram-project-react.git
```
2. Создать вирутальное окружение и установить зависимости
```
python -m venv .venv
pip install -r backend/requirements.txt
```
3. Выполнить миграции, собрать статику, создать суперпользователя, загрузить ингредиенты
```
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py importcsv
```


## Для разворачивания проекта на сервере наобходимо:
1. Установить на сервере docker и docker-compose
```
https://docs.docker.com/engine/install/ubuntu/
```
2. При необходимости создать в директории с compose.yml файл .env
```
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=backend 127.0.0.1 [::]

DB_ENGINE=django.db.backends.postgresql
DB_NAME=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
DB_HOST=db
DB_PORT=...
```
3. Собрать docker compose (миграции и сбор статики произойдут автоматически)
```
docker compose up -d --build
```
4. При необходимости создать суперпользователя и загрузить ингредиенты
```
docker exec -it container_name bash
python3 manage.py createsuperuser
python3 manage.py importcsv
exit
```


# Для Алексея:
сервер: 130.193.55.163

<ul>
  <li>superuser: alexey</li>
  <li>pass: horoshegodnya</li>
  <li>email: admin@admin.admin</li>
</ul>
