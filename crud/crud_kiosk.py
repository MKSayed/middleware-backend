from sqlalchemy import Select, insert
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.models_kiosk import Kiosk, KioskType, KioskFamily, KioskOperatorLog


class CRUDKiosk(CRUDBase):
    pass


crud_kiosk = CRUDKiosk(Kiosk)


class CRUDKioskType(CRUDBase):
    pass


crud_kiosk_type = CRUDKioskType(KioskType)


class CRUDKioskFamily(CRUDBase):
    pass


crud_kiosk_family = CRUDKioskFamily(KioskFamily)


class CRUDKioskOperatorLog(CRUDBase):
    pass


crud_kiosk_operator_log = CRUDKioskOperatorLog(KioskOperatorLog)
