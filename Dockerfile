# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

EXPOSE 8000
ENTRYPOINT [ "bash", "entrypoint.sh" ]