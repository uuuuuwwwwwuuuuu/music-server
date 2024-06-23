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

RUN pip install --upgrade pip

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install django-cors-headers
RUN pip install pillow


# Выполняем миграции и собираем статику
RUN python manage.py migrate

# Указываем команду для запуска сервера
CMD ["gunicorn", "server.wsgi:application"]
