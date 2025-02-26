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

# Если каталог alembic отсутствует, инициализируем его
if [ ! -d "/app/alembic" ]; then
    echo "🚀 Инициализация Alembic..."
    alembic init alembic
fi

# Обновляем конфигурацию Alembic
echo "🔧 Настройка Alembic..."
sed -i "s|sqlalchemy.url =.*|sqlalchemy.url = postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB|" /app/alembic.ini

# Создаём папку для версий миграций, если её нет
mkdir -p /app/alembic/versions

# Если нет миграций, создаём начальную
if [ ! "$(ls -A /app/alembic/versions)" ]; then
    echo "🚀 Создание первой миграции..."
    alembic revision --autogenerate -m "Initial migration"
fi

# Применяем миграции
echo "🔄 Применение миграций..."
alembic upgrade head

echo "🚀 Запуск приложения..."
exec uvicorn myapp.main:app --host 0.0.0.0 --port 8000
