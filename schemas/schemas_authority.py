from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    num: int
    name: str


class TransactionKioskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    active: str
    expiry_date: date
    creation_date: date
    fk_applicationnum: int


class AuthorityBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    serial: int
    start_date: date
    end_date: Optional[date] = None
    active: Optional[str] = None
    fk_transaction_number: int
    fk_authorized_rnumber: int


class AuthorizedRoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    name: Optional[str] = None
    creation_date: Optional[date] = None
    expiry_date: Optional[date] = None


class AssignedRoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    active: Optional[str] = None
    creation_date: date
    fk_authorized_rnumber: int
    fk_userid: int

