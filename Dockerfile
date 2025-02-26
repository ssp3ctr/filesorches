# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Убеждаемся, что БД доступна перед миграциями
# CMD bash -c "while !</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT; do sleep 1; done; alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["sh", "-c", "python wait_for_db.py && alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]