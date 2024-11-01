#!/bin/bash

# Задаем переменные
LOGIN="abc123333"  # Ваш логин
MATRIX_FILE="Matrix_JGL009.mtx"  # Укажите путь к файлу матрицы

# Отправляем POST-запрос к API FastAPI
# Отправляем POST-запрос к API FastAPI
curl -X POST "http://localhost:8001/save_matrix" \
     -H "Content-Type: multipart/form-data" \
     -F "login=$LOGIN" \
     -F "matrix_file=@$MATRIX_FILE"

echo ""
# Проверяем статус ответа
if [ $? -eq 0 ]; then
    echo "Request sent successfully"
else
    echo "Failed to send request"
fi
