from fastapi import (
    FastAPI,
    Depends,
)
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from app.dependencies import get_db
from sqlalchemy.orm import Session
from .database import engine, Base
from . import crud, schemas
import logging
import sys

Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{provider}/{user_id}", response_model=schemas.UserInfo)
def get(provider: str, user_id: str, db: Session = Depends(get_db)):
    user_info = crud.get_user_info(db, f"{provider}/{user_id}")
    return user_info


@app.post("/new", response_model=schemas.UserInfo, status_code=HTTPStatus.CREATED)
def create_user_info(user_info: schemas.UserInfoCreate, db: Session = Depends(get_db)):
    return crud.create_user_info(db, user_info)
