# filesorches

storage-orchestrator/
│── app/
│   ├── adapters/            # Адаптеры для различных систем хранения (S3, GWM, TCP)
│   │   ├── base.py          # Базовый класс адаптера
│   │   ├── s3_adapter.py    # AWS S3
│   │   ├── gwm_adapter.py   # Google Cloud Storage (GWM)
│   │   ├── tcp_adapter.py   # TCP хранилище
│   ├── api/                 # API-эндпоинты FastAPI
│   │   ├── v1/              # Версия API
│   │   │   ├── storage.py   # Роуты для работы с хранилищем
│   ├── core/                # Основные настройки и зависимости
│   │   ├── config.py        # Конфигурация приложения (ENV, Keycloak, адаптеры)
│   │   ├── security.py      # Авторизация через Keycloak
│   │   ├── dependencies.py  # Зависимости для API
│   ├── services/            # Сервисный слой
│   │   ├── storage_service.py # Логика сохранения файла в адаптер
│   ├── models/              # Pydantic-модели запросов и ответов
│   │   ├── file.py          # Модель для загрузки файлов
│   ├── main.py              # Точка входа FastAPI
│── tests/                   # Тесты
│── .env                     # Переменные окружения
│── docker-compose.yml        # Конфигурация Docker
│── Dockerfile                # Docker-образ
│── requirements.txt          # Зависимости
│── README.md                 # Документация