# Проектная работа 10 спринта

Проектные работы в этом модуле в команде. Задания на спринт вы найдёте внутри тем.

Ссылка на репозиторий - https://github.com/bogatovad/notifications_sprint_1

---
## Используемые технологии

- `Django` - админка для формирования текста шаблонов и мгновенной отправки уведомления пользователю/группе пользователей
- `PostgreSQL` - БД для хранения информации о шаблонах, уведомлениях, пользователях
- `FastAPI` - сервис нотификаций - API для отправки уведомлений в очередь RabbitMQ - внутри сервиса уведомлений и из внешних сервисов (напр. из сервиса Auth)
- `Clickhouse` - хранение информации об отправленных уведомлениях.
---
## Сборка и запуск
Создать и заполнить .env из .env.example в папке `envs`.  
Из корневой папки для сборки проекта выполнить:
- `make build`

Для запуска:
- `make up`

## Для создания суперпользователя:
- `make superuser`

## Схема сервиса
![](docs/images/schema.png?raw=true "Схема сервиса")

---

## Схема БД

![](docs/images/schema_db.png "Схема сервиса")

### Поля таблиц БД.


#### Template
`slug` - PK шаблона  
`title` - Заголовок  
`description` - Описание  
`content` - Текст шаблона

#### Notification
`template` - FK на шаблон  
`name` - Название шаблона, определяет имя очереди, в которую полетит уведомление  
`type` - Тип рассылки (одиночная/групповая)   
`users` - Пользователи, кому отправляется рассылка  
`groups` - Группа пользователей для рассылки  

---
### Отправка уведомления из админки

Необходимо создать Template, далее создать Notification - выбрать шаблон, тип рассылки, пользователей и/или группу(-ы) пользователей.
Затем выделить нужное уведомление  и ввыпадающем окне выбрать "Отправить уведомление пользователям"
![img.png](docs/images/admin.png)

---

## Отправка уведомления из других сервисов
Отправляем запрос, например с такими данными
```
{
    "receiver": "9de57835-28b7-4cc7-be46-95a0fb1b17c1",
    "event_name": "statistic",
    "type": "personal",
    "context": {"title": "new_films", "email": "ivan@yandex.ru", films: [{"id": 1, "title": ..., "date":..., "description": ...}]}
}
```

```
curl --location --request GET '127.0.0.1:8080/api/v1/send-notification/email' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=mKjF1tJ1h0WVkk9XM99EP2MAqP8i8cdSDAmcEBVhFsSxuIXaS3ROG87umafmJqcF' \
--data '{
    "receiver": "9de57835-28b7-4cc7-be46-95a0fb1b17c1",
    "event_name": "statistic",
    "type": "personal",
    "context": {"title": "new_films", "email": "ivan@yandex.ru", films: [{"id": 1, "title": ..., "date":..., "description": ...}]}
}'
```

- `receiver` - Один uuid в случае персональной рассылки или список uuid
- `event_name` - Название шаблона = Имя очереди
- `event_type` - Тип события 
- `type` - Тип рассылки (личная/групповая)
- `context` - Контекст для подстановки данных в шаблон 