from fastapi import FastAPI, Depends, Header, Path
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from app.dependencies import get_db
from sqlalchemy.orm import Session
from . import crud, schemas, jwt
import logging
import sys

app = FastAPI()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger(__name__)

origins = [
    "http://localhost:3000",
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
    user_auth_data = jwt.JWT.get_current_user_info_jwcrypto(x_pomerium_jwt_assertion)
    logger.info(f"User auth data is: {user_auth_data}")
    user_info = crud.get_user_info(db, user_auth_data["sub"])
    if user_info is None:
        logger.error(f"No user info available for user {user_auth_data['sub']}")
        user_info = {}
    else:
        user_info = user_info.__dict__
    return {
        **user_auth_data,
        **user_info,
    }


@app.get("/{provider}/{user_id}")
async def get_user(
    provider: str = Path(None, title="The provider of the user to get"),
    user_id: str = Path(None, title="The ID of the user to get"),
    db: Session = Depends(get_db),
):
    user_info = crud.get_user_info(db, f"{provider}/{user_id}")
    if user_info is None:
        logger.error(f"No user info available for user {provider}/{user_id}")
        return {}
    return user_info.__dict__
