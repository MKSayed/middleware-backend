from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time


class ModuleBase(BaseModel):
    ser: int
    destination: Optional[str] = Field(None, max_length=25)
    time_out: Optional[time] = None
    deviceid: Optional[str] = Field(None, max_length=10)
    target_url: Optional[str] = Field(None, max_length=40)
    organization_code: Optional[str] = Field(None, max_length=6)
    fk_connectorid: Optional[int] = None


class ConnectorBase(BaseModel):
    id: int
    name: str = Field(max_length=15)
    status: str = Field(max_length=1)
    creation_date: Optional[date] = None
    updated_date: Optional[date] = None
