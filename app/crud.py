from sqlalchemy.orm import Session
import logging

from . import models, schemas

logger = logging.getLogger(__name__)


def get_user_info(db: Session, user_id: str):
    return db.query(models.UserInfo).filter_by(user_id=user_id).first()


def create_user_info(db: Session, user_info: schemas.UserInfoCreate):
    db_user_info = models.UserInfo(**user_info.dict())
    db.add(db_user_info)
    db.commit()
    db.refresh(db_user_info)
    logger.info("New user info record created")
    return db_user_info
