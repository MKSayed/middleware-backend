from pydantic import BaseModel, Field
from typing import Optional


class AddressBase(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=35, description="abbreviation for the place")
    details: Optional[str] = Field(None, max_length=65)
    fk_police_staticd: Optional[int] = None
    fk_areacd: Optional[int] = None
    fk_address_typecd: Optional[int] = None


class AddressTypeBase(BaseModel):
    cd: int
    descr: str = Field(max_length=30)


class AreaBase(BaseModel):
    cd: int
    descr: str = Field(max_length=20)


class PoliceStationBase(BaseModel):
    cd: int
    descr: str = Field(max_length=20)
