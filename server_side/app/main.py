from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCredentials(BaseModel):
    login: str
    password: str

@app.post("/login")
async def login(credentials: UserCredentials):
    return {"login": credentials.login, "password": credentials.password}
