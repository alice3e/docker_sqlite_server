# main.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
import httpx
import os
from mongo_service import save_matrix_to_db  # Импортируем функцию из mongo.py

# Получаем URL из переменной окружения
sqlite_url = os.getenv("SQLITE_URL", "http://localhost:8000/id_request")

app = FastAPI()

# Pydantic модель для получения данных
class UserInput(BaseModel):
    login: str

async def get_user_id(credentials: UserInput):
    return 123
    # print(f"Attempting request for user: {credentials.login}")

    # # Формируем запрос к серверу SQLite для получения ID пользователя
    # login_data = {"login": credentials.login}

    # async with httpx.AsyncClient() as client:
    #     response = await client.post(sqlite_url, json=login_data)
    #     if response.status_code == 200:
    #         user_data = response.json()
    #         user_id = user_data.get("user_id")
    #         print(f"User ID retrieved: {user_id}")
    #         return user_id
    #     else:
    #         print(f"Failed to retrieve user ID: {response.text}")
    #         raise HTTPException(status_code=response.status_code, detail="Failed to retrieve user ID")

# API для сохранения матрицы от пользователя
@app.post("/save_matrix")
async def save_matrix(credentials: UserInput, matrix_file: UploadFile = File(...)):
    user_id = await get_user_id(credentials)
    # Сохранение загруженного файла .mtx
    matrix_content = await matrix_file.read()  # Чтение содержимого файла
    await save_matrix_to_db(user_id, matrix_content)  # Сохранение матрицы

    return {"message": "Matrix saved successfully", "user_id": user_id}


