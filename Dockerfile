# Используем официальный образ Python
FROM python:3.9

# Устанавливаем зависимости системы
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY . /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install django-cors-headers
RUN pip install pillow

# Выполняем миграции и собираем статику
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Указываем команду для запуска сервера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server.wsgi:application"]
