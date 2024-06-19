from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, Annotated, ClassVar
from datetime import date, datetime


class ServiceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    ar_name: str | None = Field(None, max_length=40)
    eng_name: str | None = Field(None, max_length=40)
    fk_moduleid: int | None = None
    # fk_serviceid: int | None = None
    # fk_service_grouno: int | None = None
    fk_providerid: int | None = None


class ServiceDisplay(ServiceBase):
    fk_providerid: ClassVar
    provider: "ProviderBase"
    service_price: "ServicePriceDisplay"
    service_groups: list["ServiceGroupBase"] | None = None


class ServiceDisplayShort(ServiceBase):
    fk_moduleid: ClassVar
    fk_service_grouno: ClassVar
    fk_providerid: ClassVar


class ServiceCreate(ServiceBase):
    price_type: str
    price_value: float
    max_value: float
    fk_currencyid: int


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


class ServiceGroupBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    no: int
    name: str = Field(max_length=45)


class ServiceParameterBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ser: int
    service_value: str = Field(max_length=200)
    fk_serviceid: str = Field(max_length=5)
    fk_service_paracd: Optional[int] = None


class ServiceParameterTypeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cd: int
    descr: Optional[str] = Field(None, max_length=35)
    constancy: Optional[str] = Field(None, max_length=1)
    direction: Optional[str] = Field(None, max_length=1)


class ServicePriceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    stdt: date
    enddt: date | None
    price_value: Decimal = Field(max_digits=6, decimal_places=2)
    max_value: Annotated[Decimal, Field(max_digits=6, decimal_places=2)] | None = None
    type: str | None = Field(None, max_length=8)
    list_value: str | None = Field(None, max_length=36)
    fk_serviceid: int | None = None
    fk_currencyid: int | None = None


class ServicePriceDisplay(ServicePriceBase):
    id: ClassVar
    stdt: ClassVar
    enddt: ClassVar
    fk_serviceid: ClassVar
    fk_currencyid: ClassVar


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
