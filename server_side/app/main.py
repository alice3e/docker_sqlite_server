from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import sql_service as sq # sql_service.py
import bcrypt

app = FastAPI()

# Создаем таблицы при старте приложения
sq.create_db_and_tables()

# Pydantic модель для валидации данных
class UserCredentials(BaseModel):
    name: str
    email: str
    login: str
    password: str
    
# API для входа пользователя
@app.post("/login")
async def login_user(credentials: UserCredentials, db: Session = Depends(sq.get_db_session)):
    # Проверка существования пользователя по логину
    user = sq.get_user_by_login(db, credentials.login)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid login or password")

    # Проверка пароля
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid login or password")

    return {"message": "Login successful", "user_id": user.id}

# API для регистрации нового пользователя
@app.post("/register")
async def register_user(credentials: UserCredentials, db: Session = Depends(sq.get_db_session)):
    print(credentials)
    # Проверка, есть ли пользователь с таким логином или email
    email_exists = sq.get_user_by_email(db, credentials.email)
    login_exists = sq.get_user_by_login(db, credentials.login)
    if email_exists:

        raise HTTPException(status_code=400, detail="User with this email already exists")
    elif login_exists:
        print(f'User with this login already exists - {credentials.login}')
        raise HTTPException(status_code=400, detail="User with this login already exists")
    else:
    # Добавляем нового пользователя
        new_user = sq.add_user(db, credentials.name, credentials.email, credentials.login, credentials.password)
        return {"message": "Registration successful", "user_id": new_user.id}
