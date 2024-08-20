from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Annotated, ClassVar, List
from datetime import datetime


from schemas.schemas_service import ServiceBase, ParamTypeBase, ParamLocBase


class ModuleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: Annotated[str, Field(max_length=15, min_length=2)]
    status: Annotated[str, Field(max_length=1)]
    description: Annotated[str, Field(max_length=500)]
    base_url: str
    timeout: int | None
    created: datetime | None = None
    updated: datetime | None = None
    fk_connector_id: int
    is_xml: bool


class ModuleCreate(ModuleBase):
    id: ClassVar
    created: ClassVar
    updated: ClassVar
    module_params: List["ModuleParameterCreateWithoutFK"]


class ModuleParameterBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    key: Annotated[str, Field(max_length=200)]
    value: str | None = None
    description: Annotated[str, Field(max_length=500)]
    parent_id: int | None = None
    fk_param_type_cd: int
    fk_param_loc_cd: int
    # created: datetime | None = None
    # updated: datetime | None = None
    fk_module_id: int
    type: ParamTypeBase
    location: ParamLocBase
    is_optional: bool
    is_client: bool


class ModuleParameterCreate(ModuleParameterBase):
    # Type and location in relationships not the actual foreign keys
    type: ClassVar
    location: ClassVar
    id: ClassVar


class ModuleParameterCreateWithoutFK(ModuleParameterCreate):
    fk_module_id: ClassVar


class ModuleParameterDisplayWithChildren(ModuleParameterBase):
    children: List[ModuleParameterBase] = []


class ConnectorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str = Field(max_length=15)
    status: str = Field(max_length=1)
    created: datetime | None = None
    updated: datetime | None = None


class ConnectorDisplay(ConnectorBase):
    service_count: int


class ConnectorDisplayShort(ConnectorBase):
    id: int
    status: ClassVar
    created: ClassVar
    updated: ClassVar
