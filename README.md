# mailing

Тестовое задание - Сервис уведомлений

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Описание

### Реализовано API:

1. добавления нового клиента в справочник со всеми его атрибутами
2. обновления данных атрибутов клиента
3. удаления клиента из справочника
4. добавления новой рассылки со всеми её атрибутами
5. получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
6. получения детальной статистики отправленных сообщений по конкретной рассылке
7. обновления атрибутов рассылки
8. удаления рассылки
9. обработки активных рассылок и отправки сообщений клиентам


### Дополнительное задание:

1. Подготовлен docker-compose для всех сервисов(local/production)
2. По адресу `/api/docs/` страница со Swagger
3. Обработаны возможные ошибки с удаленного сервиса(для отправки сообщений)
4. Логирование. Библиотека `loguru`

## Запуск

1. Билд проекта:
    ```
    sudo ./scripts/build_local.sh
   ```
   

2. Запуск проекта:
    ```
   sudo ./scripts/up_local.sh
   ```

3. Создание суперпользователя:
    ```
   sudo ./scripts/manage_local.sh createsuperuser
   ```
   
<br>

#### P.S. : Нужно перейти в `Административную панель - Periodic Tasks` и убедиться в наличие celery задачи - `Check Tasks`.

### Стек:

1. Django Rest Framework
2. Celery & Django Celery Beat
3. Flower
4. Docker & Docker compose
5. Swagger
6. Django Cookiecutter
7. Postgres
8. Traefik
