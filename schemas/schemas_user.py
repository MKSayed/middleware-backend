from datetime import date, time
from typing import Optional, ClassVar

from pydantic import BaseModel, ConfigDict


class UserTypeBase(BaseModel):
    cd: int
    descr: str


# Shared properties
class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    username: str
    name: str
    password: str
    national_id: Optional[str] = None
    tax_id: Optional[int] = None
    fk_user_typecd: Optional[int] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    id: ClassVar[Optional[int]]
    tax_id: ClassVar[Optional[int]]
    fk_user_typecd: ClassVar[Optional[int]]


class UserLogBase(BaseModel):
    date: date
    time: time
    fk_userid: int


class UserLogHistoryBase(BaseModel):
    old_data: str
    fk_user_logdate: date
    fk_user_logtime: time
    fk_user_logfk_userid: int


class UserLogDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    time: time
    fk_userid: int
    user: UserBase


class UserDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    name: str
    fk_user_typecd: Optional[int]
    logs: list[UserLogBase]


