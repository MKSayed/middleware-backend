from sqlalchemy import Select, insert
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.models_commission import PaymentType, CommissionType, CommissionValueType, CommissionGroup


class CRUDPaymentType(CRUDBase):
    pass


crud_payment_type = CRUDPaymentType(PaymentType)


class CRUDCommissionValueType(CRUDBase):
    pass


crud_commission_value_type = CRUDCommissionValueType(CommissionValueType)


class CRUDCommissionType(CRUDBase):
    pass


crud_commission_type = CRUDCommissionType(CommissionType)


class CRUDCommissionGroup(CRUDBase):
    pass


crud_commission_group = CRUDCommissionGroup(CommissionGroup)
