# Проектная работа 10 спринта

Проектные работы в этом модуле в команде. Задания на спринт вы найдёте внутри тем.

Ссылка на репозиторий - https://github.com/bogatovad/notifications_sprint_1


## Сборка и запуск
Создать и заполнить .env из .env.example в папке `envs`.  
Из корневой папки для сборки проекта выполнить:
- `make build`

Для запуска:
- `make up`

## Для создания суперпользователя:
- `make superuser`

## Схема сервиса
![](schemas/schema.png?raw=true "Схема сервиса")

## Схема БД

![](schemas/schema_db.png "Схема сервиса")

## Пример запроса для Notification Service
```
{
    "receiver": "9de57835-28b7-4cc7-be46-95a0fb1b17c1", # Один uuid в случае персональной рассылки или список uuid
    "event_name": "welcome", # Название шаблона = Имя очереди
    "event_type": "welcome", # Тип события
    "type": "personal", # Тип рассылки (личная/групповая0
    "context": {"title": "new_title"} # Контекст для подстановки данных в шаблон
}
```