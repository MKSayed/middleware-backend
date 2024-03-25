from fastapi import APIRouter

from api.base import RouteBase
from crud.crud_equpiment import crud_assigned_equipment, crud_equipment_type, crud_kiosk_equipment

from schemas.schemas_equipment import AssignedEquipmentBase, EquipmentTypeBase, KioskEquipmentBase

router = APIRouter()


class RouteAssignedEquipment(RouteBase):
    pass


route_assigned_equipment = RouteAssignedEquipment(model_name="assigned-equipment", base_model=AssignedEquipmentBase,
                                                  crud_model=crud_assigned_equipment, router=router)


class RouteEquipmentType(RouteBase):
    pass


route_equipment_type = RouteEquipmentType(model_name='equipment-type', base_model=EquipmentTypeBase,
                                          crud_model=crud_equipment_type, pk_name="cd", router=router)


class RouteKioskEquipment(RouteBase):
    pass


route_kiosk_equipment = RouteKioskEquipment(model_name="kiosk-equipment", base_model=KioskEquipmentBase,
                                            crud_model=crud_kiosk_equipment, pk_name="id", router=router)
