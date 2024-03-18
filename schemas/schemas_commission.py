from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CommissionGroupBase(BaseModel):
    cd: int
    descr: str = Field(max_length=50)
    value: float
    from_value: float
    to_value: float
    active_dt: Optional[date] = None
    slap: float
    fk_commission_tcd: Optional[int] = None
    fk_commission_vcd: Optional[int] = None
    fk_payment_typecd: Optional[int] = None


class CommissionTypeBase(BaseModel):
    cd: int
    descr: Optional[str] = Field(None, max_length=35)
    creation_date: Optional[date] = None


class CommissionValueTypeBase(BaseModel):
    cd: int
    descr: str = Field(max_length=20)


class PaymentTypeBase(BaseModel):
    cd: int
    descr: str = Field(max_length=30)
