from pydantic import BaseModel, Field
from typing import Optional, Annotated, ClassVar, List
from datetime import datetime


class ModuleBase(BaseModel):
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
    module_params: List["ModuleParameterWithoutFK"]


class ModuleParameter(BaseModel):
    id: Optional[int] = None
    key: str
    value: str
    description: Annotated[str, Field(max_length=100)]
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    fk_moduleid: int


class ModuleParameterCreate(ModuleParameter):
    id: ClassVar


class ModuleParameterWithoutFK(ModuleParameter):
    id: ClassVar
    fk_moduleid: ClassVar


class ConnectorBase(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=15)
    status: str = Field(max_length=1)
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
