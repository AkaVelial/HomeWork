# Установка базового образа Python
FROM python:3.10

# Копирование зависимостей и установка их
COPY apprequirements.txt .
WORKDIR /app
RUN pip install -r requirements.txt

# Копирование исходного кода
COPY ..

# Установка переменной окружения PYTHONPATH
ENV PYTHONPATH=/app

# Запуск приложения
CMD ["python", "-m", "bot"]

