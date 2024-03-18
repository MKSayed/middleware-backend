import datetime
from datetime import date
from typing import Optional, ClassVar, Union, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    num: int
    name: str = Field(max_length=30)


class PermissionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    name: str = Field(max_length=20)
    active: str = Field(max_length=3)
    expiry_date: Optional[date]
    creation_date: date
    fk_applicationnum: int


class PermissionCreate(PermissionBase):
    expiry_date: ClassVar
    creation_date: ClassVar


class PermissionUpdate(PermissionBase):
    expiry_date: ClassVar
    creation_date: ClassVar
    fk_applicationnum: ClassVar


class PermissionDisplay(PermissionBase):
    fk_applicationnum: ClassVar
    application: ApplicationBase


class AuthorityBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    serial: int
    start_date: date
    end_date: Optional[date] = None
    active: Optional[str] = Field(None, max_length=1)
    fk_permission_number: int
    fk_authorized_rnumber: int


class AuthorityCreate(AuthorityBase):
    serial: ClassVar
    end_date: ClassVar


class AuthorityUpdate(AuthorityCreate):
    fk_permission_number: ClassVar
    fk_authorized_rnumber: ClassVar
    end_date: ClassVar


class AuthorityDisplay(AuthorityBase):
    model_config = ConfigDict(from_attributes=True)

    class AuthorityPermissionDisplay(BaseModel):
        number: int
        name: str

    class AuthorityAuthorizedRoleDisplay(BaseModel):
        number: int
        name: Optional[str] = None

    fk_permission_number: ClassVar
    fk_authorized_rnumber: ClassVar
    permission: AuthorityPermissionDisplay
    authorized_role: AuthorityAuthorizedRoleDisplay


class AuthorizedRoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    name: Optional[str] = Field(None, max_length=50)
    creation_date: Optional[date] = None
    expiry_date: Optional[date] = None


class AuthorizedRoleCreate(AuthorizedRoleBase):
    creation_date: ClassVar[date]
    expiry_date: ClassVar[date]


class AssignedRoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    active: Optional[str] = Field(None, max_length=1)
    creation_date: date = Field(default_factory=date.today)
    fk_authorized_rnumber: int
    fk_userid: int

# todo create AssignedRoleCreate Class without creation_date

    # Make sure to override the field with current date if user sends it.
    # @field_validator("creation_date", mode="before")
    # @classmethod
    # def set_default_created_at(cls, v: Any):
    #     return datetime.date.today()
