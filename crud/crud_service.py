from sqlalchemy import Select, insert
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.models_service import (Service, ServiceGroup, ServicePrice, Provider, Currency, ServiceParameter,
                                   ServiceCharge, ServiceParameterType)


class CRUDService(CRUDBase):
    pass


crud_service = CRUDService(Service)


class CRUDServiceCharge(CRUDBase):
    pass


crud_service_charge = CRUDServiceCharge(ServiceCharge)


class CRUDServiceGroup(CRUDBase):
    pass


crud_service_group = CRUDServiceGroup(ServiceGroup)


class CRUDServiceParameter(CRUDBase):
    pass


crud_service_parameter = CRUDServiceParameter(ServiceParameter)


class CRUDServiceParameterType(CRUDBase):
    pass


crud_service_parameter_type = CRUDServiceParameterType(ServiceParameterType)


class CRUDServicePrice(CRUDBase):
    pass


crud_service_price = CRUDServicePrice(ServicePrice)


class CRUDProvider(CRUDBase):
    pass


crud_provider = CRUDProvider(Provider)


class CRUDCurrency(CRUDBase):
    pass


crud_currency = CRUDCurrency(Currency)
