from fastapi import APIRouter

from api.base import RouteBase
from crud.crud_kiosk import crud_kiosk, crud_kiosk_family, crud_kiosk_type, crud_kiosk_operator_log
from schemas.schemas_kiosk import (KioskBase, KioskFamilyBase, KioskTypeBase, KioskOperatorLogBase)

router = APIRouter()


class RouteKiosk(RouteBase):
    pass


route_kiosk = RouteKiosk(model_name="address", base_model=KioskBase, crud_model=crud_kiosk, pk_name="id",
                         router=router)


class RouteKioskFamily(RouteBase):
    pass


route_kiosk_family = RouteKioskFamily(model_name='address-type', base_model=KioskFamilyBase,
                                      crud_model=crud_kiosk_family, pk_name="id", router=router)


class RouteKioskType(RouteBase):
    pass


route_kiosk_type = RouteKioskType(model_name="area", base_model=KioskTypeBase, crud_model=crud_kiosk_type, pk_name="id",
                                  router=router)


class RouteKioskOperatorLog(RouteBase):
    pass


route_kiosk_operator_log = RouteKioskOperatorLog(model_name="police-station", base_model=KioskOperatorLogBase,
                                                 crud_model=crud_kiosk_operator_log, pk_name="id", router=router)
