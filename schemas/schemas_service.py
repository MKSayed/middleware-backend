from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, Annotated, ClassVar
from datetime import date, datetime
from enum import Enum


class HTTPMethodEnum(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class ServiceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    ar_name: str | None = Field(None, max_length=40)
    eng_name: str | None = Field(None, max_length=40)
    fk_module_id: int | None = None
    http_method: HTTPMethodEnum
    endpoint_path: str
    fk_provider_id: int


class ServiceDisplay(ServiceBase):
    provider: "ProviderBase"
    service_price: "ServicePriceDisplay"
    service_groups: list["ServiceGroupBase"] | None = None


class ServiceDisplayShort(ServiceBase):
    fk_module_id: ClassVar
    fk_provider_id: ClassVar


class ServiceCreate(ServiceBase):
    price_type: str
    price_value: float
    max_value: float
    fk_currency_id: int
    price_lists: list["PriceListCreate"]


class ServiceGroupBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    no: int
    name: str = Field(max_length=45)


class ServiceParameterBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    key: str = Field(max_length=200)
    value: str | None = None
    parent_id: int | None = None
    fk_service_id: int
    fk_param_type_cd: int
    fk_param_loc_cd: int
    is_optional: bool
    is_client: bool
    value_reference_id: int | None = None
    # fk_service_para_type_cd: int


class ServiceParameterCreate(ServiceParameterBase):
    id: ClassVar

# class ServiceParameterTypeBase(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#
#     cd: int
#     descr: Optional[str] = Field(None, max_length=35)
#     constancy: Optional[str] = Field(None, max_length=1)
#     direction: Optional[str] = Field(None, max_length=1)


class ParamTypeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cd: int
    descr: Annotated[str, Field(max_length=35)]


class ParamLocBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cd: int
    descr: Annotated[str, Field(max_length=35)]


class ServiceChargeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cd: int
    descr: str = Field(max_length=500)
    value: Decimal = Field(max_digits=11, decimal_places=2)
    from_value: Decimal = Field(max_digits=11, decimal_places=2)
    to_value: Decimal = Field(max_digits=11, decimal_places=2)
    active_dt: Optional[date]
    slap: Decimal = Field(max_digits=11, decimal_places=2)
    fk_commission_tcd: Optional[int] = None
    fk_commission_vcd: Optional[int] = None


class ServicePriceTypeEnum(str, Enum):
    FIXED = "FIXED"
    RANGE = "RANGE"
    LIST = "LIST"


class ServicePriceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    stdt: date
    enddt: date | None
    price_value: Annotated[Decimal, Field(max_digits=6, decimal_places=2)]
    max_value: Annotated[Decimal, Field(max_digits=6, decimal_places=2)] | None = None
    type: ServicePriceTypeEnum
    # list_value: str | None = Field(None, max_length=36)
    fk_service_id: int | None = None
    fk_currency_id: int | None = None


class ServicePriceDisplay(ServicePriceBase):
    id: ClassVar
    stdt: ClassVar
    enddt: ClassVar
    fk_service_id: ClassVar
    fk_currency_id: ClassVar


class PriceListBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    key: Annotated[str, Field(max_length=40)]
    price_value: Annotated[Decimal, Field(max_digits=6, decimal_places=2)]
    fk_service_price_id: int


class PriceListCreate(PriceListBase):
    fk_service_price_id: ClassVar


class ProviderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    ar_name: str = Field(max_length=40)
    eng_name: str = Field(max_length=40)


class CurrencyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str = Field(max_length=5)
    name: Optional[str] = Field(None, max_length=20)
    active_from: Optional[datetime] = None
    rate: Decimal = Field(max_digits=9, decimal_places=2)


class CurrencyDisplayShort(CurrencyBase):
    code: ClassVar
    active_from: ClassVar
    rate: ClassVar
