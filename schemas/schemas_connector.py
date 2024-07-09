from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Annotated, ClassVar, List
from datetime import datetime

from schemas.schemas_service import ServiceBase


class ModuleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: Annotated[str, Field(max_length=15)]
    status: Annotated[str, Field(max_length=1)]
    description: Annotated[str, Field(max_length=100)]
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    fk_connectorid: int


class ModuleCreate(ModuleBase):
    id: ClassVar
    created: ClassVar
    updated: ClassVar
    module_params: List["ModuleParameterBaseWithoutFK"]


class ModuleParameterBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    key: str
    value: str
    description: Annotated[str, Field(max_length=100)]
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    fk_moduleid: int


class ModuleParameterCreate(ModuleParameterBase):
    id: ClassVar


class ModuleParameterBaseWithoutFK(ModuleParameterBase):
    id: ClassVar
    fk_moduleid: ClassVar


class ConnectorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str = Field(max_length=15)
    status: str = Field(max_length=1)
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


class ConnectorDisplay(ConnectorBase):
    service_count: int


class ConnectorDisplayShort(ConnectorBase):
    id: int
    status: ClassVar
    created: ClassVar
    updated: ClassVar
