# Проект

AdWebsiteParser

# Stack

* FastAPI
* Postgres
* PyTelegramBotAPI

## Установка

### .ENV

```
DEBUG=True/False
DB_URL=postgresql://{user_name}:{user_pass}@localhost:5432/{db_name}
TELEGRAM_TOKEN=xxx
```

## **НАСТРОЙКА БОТА**

* Включить инлайн режим в BotFather
* Включить инлайн фитбэк (поставить 100%) в BotFather
* Установить вебхук (https://api.telegram.org/bot{token}/setWebhook?url=https://{domen}/telegram/{token})

## **Установка зависимостей:**

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

или

```bash
poetry install
```

## **БАЗА ДАННЫХ**

### Миграция ДБ

```bash
poetry run alembic upgrade head
```

### Генерация миграции (только ДЕВ)

```bash
poetry run alembic revision --autogenerate
```

### Парсер

### Запуск парсера

```bash
python run_parser.py
```

### Запуск проекта

```bash
uvicorn core.app:app --reload
```

## КОМАНДЫ

### Генерация requirements.txt

```bash
poetry export --without-hashes --format=requirements.txt > requirements.txt
```