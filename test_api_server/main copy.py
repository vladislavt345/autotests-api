from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

import hashlib

DATABASE_URL = "sqlite:///./test.db"

# Инициализация базы данных и таблицы пользователей
database = Database(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("middle_name", String, nullable=True),
    Column("hashed_password", String, nullable=False),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI(title="Test API", version="1.0.0")


class UserCreateRequest(BaseModel):
    email: EmailStr
    first_name: str = Field(..., example="Иван")
    last_name: str = Field(..., example="Иванов")
    middle_name: Optional[str] = Field(None, example="Иванович")
    password: str = Field(..., min_length=6, example="mysecret123")


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/ping", response_model=dict, summary="Проверка работоспособности")
async def ping():
    return {"message": "pong"}


def hash_password(password: str) -> str:
    # Простое sha256, в реальных проектах лучше bcrypt или argon2
    return hashlib.sha256(password.encode()).hexdigest()


@app.post("/users", response_model=UserResponse, summary="Создать нового пользователя")
async def create_user(user: UserCreateRequest):
    query = users.select().where(users.c.email == user.email)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_pw = hash_password(user.password)
    insert_query = users.insert().values(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
        hashed_password=hashed_pw,
    )
    user_id = await database.execute(insert_query)

    full_name = f"{user.last_name} {user.first_name}"
    if user.middle_name:
        full_name += f" {user.middle_name}"

    return UserResponse(id=user_id, email=user.email, full_name=full_name)


@app.delete("/users/{user_id}", summary="Удалить пользователя по ID")
async def delete_user(user_id: int = Path(..., description="ID пользователя для удаления")):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if not user:
        return {"detail": f"Пользователь с id={user_id} не найден"}

    delete_query = users.delete().where(users.c.id == user_id)
    await database.execute(delete_query)
    return {"detail": f"Пользователь с id={user_id} успешно удалён"}