from fastapi import FastAPI, Depends, Header
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from app.dependencies import get_db
from sqlalchemy.orm import Session
from .database import engine, Base
from . import crud, schemas, jwt
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


@app.post("/new", response_model=schemas.UserInfo, status_code=HTTPStatus.CREATED)
def create_user_info(user_info: schemas.UserInfoCreate, db: Session = Depends(get_db)):
    return crud.create_user_info(db, user_info)


@app.get("/me")
async def get_current_user(
    db: Session = Depends(get_db),
    x_pomerium_jwt_assertion: Optional[str] = Header(None),
):
    user_auth_data = jwt.JWT.get_current_user_info(x_pomerium_jwt_assertion)
    user_info = crud.get_user_info(db, user_auth_data["sub"])
    return {
        **user_auth_data,
        **user_info.__dict__,
    }
