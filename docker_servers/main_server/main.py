from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

app = FastAPI()

sqlite_url = None
mongo_server_url = None

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
    
# API для входа пользователя
@app.post("/login")
async def login_user(credentials: LoginCredentials):
    """
    Нужен для входа в систему
    Дейтсвия по шагам:\n
    1)получает логин и пароль\n
    2)проверяет доступность sqlite контейнера\n
    3)перенаправляет данные на sqlite сервер\n
    4)получает ответ\n
    5)отправляет ответ клиенту\n
    """
    
    pass

# API для входа пользователя
@app.post("/register")
async def register(credentials: RegisterCredentials):
    """
    Нужен для регистрации пользователя
    Дейтсвия по шагам:\n
    1)получает логин, пароль, имя, почту\n
    2)проверяет доступность sqlite контейнера\n
    3)перенаправляет данные на sqlite сервер\n
    4)получает ответ\n
    5)отправляет ответ клиенту\n
    """
    
    pass

@app.post("/save_matrix")
async def save_matrix( login: str = Form(...),  matrix_file: UploadFile = File(...) ):
    """
    Нужен для загрузки матрицы .mtx на сервер
    Дейтсвия по шагам:\n
    1)получает матрицу (.mtx), логин пользователя \n
    2)проверяет доступность mongodb контейнера\n
    3)перенаправляет данные на mongodb сервер\n
    4)получает ответ\n
    5)отправляет ответ клиенту\n
    """
    pass

@app.post("/get_matrix_names_by_user_login")
async def save_matrix( login: str = Form(...),  matrix_file: UploadFile = File(...) ):
    """
    Нужен для получения списка матриц, которые загружал пользователь
    Дейтсвия по шагам:\n
    1)получает логин пользователя \n
    2)проверяет доступность mongodb, sqlite контейнеров\n
    3)перенаправляет данные на mongodb сервер\n
    4)получает ответ\n
    5)отправляет ответ клиенту\n
    """
    pass