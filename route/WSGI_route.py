from flask import Flask

app = Flask(__name__)

@app.route('/calc/<int:x>/<int:y>/<operation>')
def calculator(x, y, operation):
    if operation == '+':
        result = x + y
    elif operation == '-':
        result = x - y
    elif operation == '*':
        result = x * y
    elif operation == '/':
        result = x / y
    return str(result)

if __name__ == '__main__':
# app.run()  # Это запуск для разработки, заменяем на Gunicorn в продакшн среде
# Запуск на Gunicorn в продакшн среде
# Указываем в качестве имени модуля 'app', а в качестве имени переменной с Flask-приложением - 'app'
# Указываем количество воркеров - 4
# Указываем хост и порт для обслуживания приложения - 127.0.0.1:5000
# Запускаем Gunicorn командой
# gunicorn app:app -w 4 -b 127.0.0.1:5000