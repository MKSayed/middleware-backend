from crud.base import CRUDBase
from models.models_connector import Connector, Module, ModuleParameter


class CRUDConnector(CRUDBase):
    pass


crud_connector = CRUDConnector(Connector)


class CRUDModule(CRUDBase):
    pass


crud_module = CRUDModule(Module)


class CRUDModuleParameter(CRUDBase):
    pass


crud_module_parameter = CRUDModuleParameter(ModuleParameter)