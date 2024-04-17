from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional, Annotated
from datetime import datetime


class KioskBase(BaseModel):
    id: int
    account_no: Decimal = Field(max_digits=10)
    ar_name: str = Field(max_length=40)
    eng_name: str = Field(max_length=40)
    descr: Optional[str] = Field(None, max_length=100)
    creation_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=1)
    deleted_flag: Optional[int] = None
    cd_part1: Optional[int] = None
    cd_part2: Optional[int] = None
    commission_check: Optional[str] = Field(None, max_length=1)
    service_group_check: Optional[str] = Field(None, max_length=1)
    service_charge_check: Optional[str] = Field(None, max_length=1)
    fk_service_grouno: Optional[int] = None
    fk_addressid: Optional[int] = None
    fk_kiosk_familyid: Optional[int] = None
    fk_commission_gcd: Optional[int] = None


class KioskFamilyBase(BaseModel):
    id: int
    account_no: Decimal = Field(max_digits=10)
    ar_name: str = Field(max_length=40)
    eng_name: str = Field(max_length=40)
    type: Optional[str] = Field(None, max_length=1)
    descr: Optional[str] = Field(None, max_length=100)
    updated_date: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=1)
    deleted_flag: Optional[int] = None
    fk_commession_gcd: Optional[int] = None
    fk_service_charcd: Optional[int] = None
    fk_service_grouno: Optional[int] = None


class KioskOperatorLogBase(BaseModel):
    id: Decimal = Field(max_digits=14)
    ip_address: Optional[str] = Field(None, max_length=15)
    entrystamp: Optional[datetime] = None
    aff_field: Decimal = Field(max_digits=10)
    aff_field2: Annotated[Decimal, Field(max_digits=10)] | None = None
    type: Optional[str] = Field(None, max_length=1)
    fk_kioskid: Optional[int] = None
    fk_permission_number: Optional[int] = None


class KioskTypeBase(BaseModel):
    id: int
    descr: str = Field(max_length=30)
