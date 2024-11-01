#!/bin/bash

# Задаем переменные
LOGIN="johndoe"  # Ваш логин
MATRIX_FILE="Matrix_JGL009.mtx"  # Укажите путь к файлу матрицы

# Отправляем POST-запрос к API FastAPI
# Отправляем POST-запрос к API FastAPI
curl -X POST "http://localhost:8001/save_matrix" \
     -H "Content-Type: multipart/form-data" \
     -F "login=$LOGIN" \
     -F "matrix_file=@$MATRIX_FILE"

echo ""

USER_ID=1  # Замените на актуальный ID пользователя
curl -X GET "http://localhost:8001/get_matrix_by_user_id/$USER_ID"

echo ""

FILENAME="Matrix_JGL009.mtx"  # Укажите имя файла матрицы
curl -X GET "http://localhost:8001/get_matrix_by_filename/$FILENAME"

echo ""

curl -X GET "http://localhost:8001/ping"
