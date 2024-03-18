from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class AssignedEquipmentBase(BaseModel):
    timestamp: Optional[datetime] = None
    start_date: date
    end_date: Optional[date] = None
    status: Optional[int] = None
    fk_kioskid: int
    fk_kiosk_equipmid: int


class EquipmentTypeBase(BaseModel):
    cd: int
    descr: Optional[str] = Field(None, max_length=50)
    status: Optional[int] = None


class KioskEquipmentBase(BaseModel):
    id: int
    descr: Optional[str] = Field(None, max_length=100)
    component_ser_num: Optional[str] = Field(None, max_length=20)
    component_ip_address: Optional[str] = Field(None, max_length=15)
    creation_date: Optional[datetime] = None
    status: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    fk_equipment_tycd: Optional[int] = None
