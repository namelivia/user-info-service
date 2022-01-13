from pydantic import BaseModel, Field
from typing import Optional


class UserInfoBase(BaseModel):
    user_id: str = Field(title="User id on the external provider")
    name: Optional[str] = Field(title="User name")
    locale: Optional[str] = Field(title="User locale")


class UserInfoCreate(UserInfoBase):
    pass


class UserInfo(UserInfoBase):
    id: int

    class Config:
        orm_mode = True
