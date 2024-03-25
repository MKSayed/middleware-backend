from sqlalchemy import Select, insert
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.models_equipment import AssignedEquipment, EquipmentType, KioskEquipment


class CRUDAssignedEquipment(CRUDBase):
    pass


crud_assigned_equipment = CRUDAssignedEquipment(AssignedEquipment)


class CRUDEquipmentType(CRUDBase):
    pass


crud_equipment_type = CRUDEquipmentType(EquipmentType)


class CRUDKioskEquipment(CRUDBase):
    pass


crud_kiosk_equipment = CRUDKioskEquipment(KioskEquipment)
