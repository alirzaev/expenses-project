# Веб-приложение для учета расходов

## Bootstrapping

```
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
```

## Heroku

|Переменная              |Описание                                       |
|------------------------|-----------------------------------------------|
|`DJANGO_SETTINGS_MODULE`|Модуль с настройками (`config.settings_heroku`)|
|`DATABASE_URL`          |URL базы данных                                |
|`SECRET_KEY`            |Секретный ключ                                 |