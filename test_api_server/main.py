from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine, Base
from models import Cat
from pydantic import BaseModel

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cats API")

# Pydantic схемы
class CatCreate(BaseModel):
    name: str
    breed: str
    age: int

class CatRead(CatCreate):
    id: int

    class Config:
        orm_mode = True

# Зависимость: сессия БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cats", response_model=CatRead)
def create_cat(cat: CatCreate, db: Session = Depends(get_db)):
    db_cat = Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@app.get("/cats", response_model=List[CatRead])
def read_cats(db: Session = Depends(get_db)):
    return db.query(Cat).all()
