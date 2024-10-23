from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sql_service import create_db_and_tables, add_user, get_user_by_email_or_login, get_db_session

app = FastAPI()

# Создаем таблицы при старте приложения
create_db_and_tables()

# Pydantic модель для валидации данных
class UserCredentials(BaseModel):
    name: str
    email: str
    login: str
    password: str

# API для регистрации нового пользователя
@app.post("/login")
async def register_user(credentials: UserCredentials, db: Session = Depends(get_db_session)):
    
    # Проверка, есть ли пользователь с таким логином или email
    user_exists = get_user_by_email_or_login(db, credentials.email, credentials.login)
    if user_exists:
        raise HTTPException(status_code=400, detail="User with this login or email already exists")

    # Добавляем нового пользователя
    new_user = add_user(db, credentials.name, credentials.email, credentials.login, credentials.password)

    return {"message": "Registration successful", "user_id": new_user.id}
