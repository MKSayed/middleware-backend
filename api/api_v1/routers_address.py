from typing import List

from fastapi import APIRouter

from api.base import RouteBase
from crud.crud_address import crud_address, crud_address_type, crud_area, crud_police_station

from schemas.schemas_adress import (AddressBase, AddressTypeBase, AreaBase, PoliceStationBase)

router = APIRouter()


class RouteAddress(RouteBase):
    pass


route_address = RouteAddress(model_name="address", base_model=AddressBase, crud_model=crud_address, pk_name="id",
                             router=router)


class RouteAddressType(RouteBase):
    pass


route_address_type = RouteAddressType(model_name='address-type', base_model=AddressTypeBase,
                                      crud_model=crud_address_type, pk_name="cd", router=router)


class RouteArea(RouteBase):
    pass


route_area = RouteArea(model_name="area", base_model=AreaBase, crud_model=crud_area, pk_name="CD", router=router)


class RoutePoliceStation(RouteBase):
    pass


route_police_station = RoutePoliceStation(model_name="police-station", base_model=PoliceStationBase,
                                          crud_model=crud_police_station, pk_name="cd", router=router)
