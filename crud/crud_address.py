from sqlalchemy import Select, insert
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.models_address import Address, AddressType, Area, PoliceStation


class CRUDAddress(CRUDBase):
    pass


crud_address = CRUDAddress(Address)


class CRUDAddressType(CRUDBase):
    pass


crud_address_type = CRUDAddressType(AddressType)


class CRUDArea(CRUDBase):
    pass


crud_area = CRUDArea(Area)


class CRUDPoliceStation(CRUDBase):
    pass


crud_police_station = CRUDPoliceStation(PoliceStation)
