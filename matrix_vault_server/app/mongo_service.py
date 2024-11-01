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

async def get_matrix_from_db(file_id):
    # Извлечение матрицы из GridFS по ID
    matrix_data = grid_fs.get(file_id).read()
    return matrix_data

async def find_matrices_by_user_id(user_id: int):
    # Поиск всех матриц для конкретного пользователя
    matrices = []
    for matrix in grid_fs.find({"user_id": user_id}):
        matrices.append({"file_id": str(matrix._id), "filename": matrix.filename})
    return matrices

async def find_matrix_by_filename(filename: str):
    # Поиск матрицы по имени файла
    matrix = grid_fs.find_one({"filename": filename})
    return matrix
