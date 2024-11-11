from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

# Загрузка конфигураций
sqlite_url = os.getenv("SQLITE_URL")
mongo_server_url = os.getenv("MONGO_SERVER_URL")

# Pydantic модель для регистрации пользователя
class RegisterCredentials(BaseModel):
    name: str
    email: str
    login: str
    password: str
    
# Pydantic модель для входа
class LoginCredentials(BaseModel):
    login: str
    password: str
    
# Pydantic модель для получения id
class IdCredentials(BaseModel):
    login: str

# Функция для проверки доступности серверов
async def check_server_availability(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return True
    except httpx.RequestError:
        return False
    return False

# API для входа пользователя
@app.post("/login")
async def login_user(credentials: LoginCredentials):
    # Проверка доступности SQLite сервера
    if not await check_server_availability(f"{sqlite_url}/status"):
        raise HTTPException(status_code=503, detail="SQLite сервер недоступен")

    # Перенаправление данных на SQLite сервер
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{sqlite_url}/login", json=credentials.dict())
        
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Ошибка входа")
    
    return response.json()

# API для регистрации пользователя
@app.post("/register")
async def register(credentials: RegisterCredentials):
    if not await check_server_availability(f"{sqlite_url}/status"):
        raise HTTPException(status_code=503, detail="SQLite сервер недоступен")

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{sqlite_url}/register", json=credentials.dict())
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Ошибка регистрации")
    
    return response.json()

@app.post("/save_matrix")
async def save_matrix(login: str = Form(...), matrix_file: UploadFile = File(...)):
    if not await check_server_availability(f"{mongo_server_url}/status"):
        raise HTTPException(status_code=503, detail="MongoDB сервер недоступен")

    async with httpx.AsyncClient() as client:
        files = {'matrix_file': (matrix_file.filename, await matrix_file.read())}
        data = {'login': login}
        response = await client.post(f"{mongo_server_url}/save_matrix", data=data, files=files)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Ошибка при сохранении матрицы")
    
    return response.json()

@app.post("/get_matrix_names_by_user_login")
async def get_matrix_names_by_user_login(credentials: IdCredentials):
    if not await check_server_availability(f"{mongo_server_url}/status") or not await check_server_availability(f"{sqlite_url}/status"):
        raise HTTPException(status_code=503, detail="Один из серверов недоступен")

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{mongo_server_url}/get_matrix_names", json=credentials.dict())
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Ошибка при получении списка матриц")
    
    return response.json()
