from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time


class ModuleBase(BaseModel):
    id: int
    key: int
    value: int
    fk_connectorid: Optional[int] = None


class ConnectorBase(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=15)
    status: str = Field(max_length=1)
    creation_date: Optional[date] = None
    updated_date: Optional[date] = None
