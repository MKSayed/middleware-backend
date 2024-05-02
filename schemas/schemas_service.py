from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, Annotated, ClassVar
from datetime import date, datetime


class ServiceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(max_length=5)
    ar_name: Optional[str] = Field(None, max_length=40)
    eng_name: Optional[str] = Field(None, max_length=40)
    fk_moduleser: Optional[int] = None
    fk_service_grouno: Optional[int] = None
    fk_providerid: Optional[int] = None


class ServiceDisplayShort(ServiceBase):
    fk_moduleser: ClassVar
    fk_service_grouno: ClassVar
    fk_providerid: ClassVar


class ServiceChargeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cd: int
    descr: str = Field(max_length=50)
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
    enddt: Optional[date]
    price_value: Decimal = Field(max_digits=8, decimal_places=2)
    max_value: Annotated[Decimal, Field(max_digits=8, decimal_places=2)] | None = None
    type: Optional[str] = Field(None, max_length=8)
    list_value: Optional[str] = Field(None, max_length=36)
    fk_serviceid: Optional[str] = Field(None, max_length=5)
    fk_currencyid: Optional[int] = None


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
