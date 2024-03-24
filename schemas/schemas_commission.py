from pydantic import BaseModel, Field
from typing import Optional, ClassVar
from decimal import Decimal
from datetime import date


class CommissionGroupBase(BaseModel):
    cd: int
    descr: str = Field(max_length=50)
    value: Decimal = Field(max_digits=11, decimal_places=2)
    from_value: Decimal = Field(max_digits=11, decimal_places=2)
    to_value: Decimal = Field(max_digits=11, decimal_places=2)
    active_dt: Optional[date] = None
    slap: Decimal = Field(max_digits=11, decimal_places=2)
    fk_commission_tcd: Optional[int] = None
    fk_commission_vcd: Optional[int] = None
    fk_payment_typecd: Optional[int] = None


class CommissionTypeBase(BaseModel):
    cd: int
    descr: Optional[str] = Field(None, max_length=35)
    creation_date: Optional[date] = None


class CommissionTypeCreate(CommissionTypeBase):
    creation_date: ClassVar


class CommissionValueTypeBase(BaseModel):
    cd: int
    descr: str = Field(max_length=20)


class PaymentTypeBase(BaseModel):
    cd: int
    descr: str = Field(max_length=30)
