#!/bin/sh
set -e

# Загружаем переменные из .env (если запускается вручную)
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "⏳ Ожидание запуска PostgreSQL на ${POSTGRES_HOST}:${POSTGRES_PORT}..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  sleep 1
done
echo "✅ PostgreSQL доступен!"

# Проверяем наличие каталога alembic
if [ ! -d "/app/alembic" ]; then
    echo "🚀 Инициализация Alembic..."
    alembic init alembic
fi

# Перемещаем и обновляем env.py
if [ -f "/app/env.py" ]; then
    echo "🔧 Перемещение env.py в alembic..."
    mv /app/env.py /app/alembic/env.py
fi

# Настроим Alembic.ini
echo "🔧 Настройка Alembic..."
sed -i "s|sqlalchemy.url =.*|sqlalchemy.url = postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB|" /app/alembic.ini

# Создаём папку для версий миграций, если её нет
mkdir -p /app/alembic/versions

# Получаем текущую версию из базы данных и из файловой системы
DB_VERSION=$(alembic current --verbose | grep 'Current:' | awk '{print $3}')
LATEST_VERSION=$(alembic heads | awk '{print $1}')

# Проверяем, если в базе есть миграция, а в файлах их нет
if [ -n "$DB_VERSION" ] && [ -z "$LATEST_VERSION" ]; then
    echo "⚠️ В базе данных есть миграция ($DB_VERSION), но файлы миграции отсутствуют!"
    echo "🔄 Создаём пустую миграцию, чтобы синхронизировать состояние..."
    alembic stamp head
    alembic revision --autogenerate -m "Restore missing migrations"
    alembic upgrade head
elif [ -z "$LATEST_VERSION" ] || [ "$DB_VERSION" != "$LATEST_VERSION" ]; then
    echo "⚠️ Версия базы данных отличается от файловой системы. Обновляем..."
    alembic stamp head
    alembic revision --autogenerate -m "Auto migration"
    alembic upgrade head
else
    echo "✅ Версия миграций в базе актуальна. Применяем обновления..."
    alembic upgrade head
fi

# Запуск приложения
echo "🚀 Запуск приложения..."
exec uvicorn main:app --host 0.0.0.0 --port 8000