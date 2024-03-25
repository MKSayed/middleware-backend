from sqlalchemy import Select, insert
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.models_connector import Connector, Module


class CRUDConnector(CRUDBase):
    pass


crud_connector = CRUDConnector(Connector)


class CRUDModule(CRUDBase):
    pass


crud_module = CRUDModule(Module)
