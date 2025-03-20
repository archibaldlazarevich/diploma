#  Сервис микроблогов (Клон Twitter)

##  Описание проекта
Данный проект представляет собой **бэкенд для корпоративного сервиса микроблогов**, аналогичного Twitter. 
Фронтенд уже реализован, а текущий репозиторий содержит серверную часть. 

Бэкенд разработан с использованием **FastAPI**, базы данных **PostgreSQL** и развернут с помощью **Docker Compose**. 
Также реализованы **юнит-тесты (pytest)** и проверка кода линтерами **mypy, flake8, black, isort**. 

##  Технологии
- **FastAPI** — веб-фреймворк для создания API 
- **PostgreSQL** — реляционная база данных 
- **Nginx** — проксирование запросов 
- **Docker, Docker Compose** — контейнеризация 
- **pytest** — тестирование 
- **mypy, flake8, black, isort** — статический анализ кода 

##  Установка и запуск

###  Клонирование репозитория
```
git clone https://github.com/archibaldlazarevich/diploma.git
```

###  Запуск в Docker
```
docker-compose up -d
```
Приложение будет доступно по адресу **http://localhost** 
Документация API (Swagger): **http://localhost:8000/docs**

###  Остановка сервиса
```
docker-compose down
```

##  Функционал API
-  **Создание и удаление твитов**
-  **Лайки и отмена лайков**
-  **Подписка/отписка на пользователей**
-  **Лента твитов**
-  **Добавление изображений к твиту**
-  **Просмотр профилей пользователей**

Полная документация API доступна в Swagger после запуска проекта.

##  Тестирование
Запуск всех тестов:
```
pytest
```
Проверка кода линтерами:
```
flake8 .
black --check .
isort --check-only .
mypy .
```
