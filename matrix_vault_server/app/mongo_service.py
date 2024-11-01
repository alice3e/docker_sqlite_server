import os
from pymongo import MongoClient
from gridfs import GridFS

# Получаем URL MongoDB из переменной окружения
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URL)

# Создаем базу данных и GridFS
db = client["mydatabase"]  # Замените на имя вашей базы данных
grid_fs = GridFS(db)  # Создаем экземпляр GridFS

async def save_matrix_to_db(user_id: int, matrix_name: str, matrix_content: bytes):
    # Сохранение матрицы в GridFS
    matrix_record = {
        "user_id": user_id,
        "filename": f"{matrix_name}.mtx"  # Уникальное имя файла
    }

    # Запись матрицы в GridFS
    grid_fs.put(matrix_content, **matrix_record)  # Используем метод put для сохранения

    return {"message": "Matrix saved to GridFS successfully", "user_id": user_id, "matrix_name": matrix_name}
