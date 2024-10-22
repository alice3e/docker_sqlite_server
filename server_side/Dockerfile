# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY app/requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем код приложения
COPY app/ .

# Запускаем приложение с uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
