from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import httpx
import os  # Импортируем модуль os для работы с переменными окружения

# Получаем URL из переменной окружения
sqlite_url = os.getenv("SQLITE_URL", "http://localhost:8000/id_request")  # Значение по умолчанию

app = FastAPI()

# Pydantic модель для получения данных
class UserInput(BaseModel):
    login: str
    # matrix: matrix.mtx  # Закомментировано, пока не нужно
    
# Pydantic модель для запроса в SQLite
class SqliteRequest(BaseModel):
    login: str
    uniq_id: int


# API для сохранения матрицы от пользователя
@app.post("/save_matrix")
async def save_matrix(credentials: UserInput):
    print(f"Attempting request for user: {credentials.login}")
    
    # Формируем запрос к серверу SQLite для получения ID пользователя
    login_data = {"login": credentials.login, "password": "user_password"}  # Замените на реальный пароль

    async with httpx.AsyncClient() as client:
        response = await client.post(sqlite_url, json=login_data)
        
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data.get("user_id")
            print(f"User ID retrieved: {user_id}")
            # Здесь вы можете сохранить матрицу или выполнить другие действия с user_id
            return {"message": "Matrix saved successfully", "user_id": user_id}
        else:
            print(f"Failed to retrieve user ID: {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve user ID")
