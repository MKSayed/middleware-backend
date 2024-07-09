from sqlalchemy import func, select
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.models_connector import Connector, Module, ModuleParameter
from models.models_service import Service


class CRUDConnector(CRUDBase):

    @staticmethod
    def get_all_with_service_count(db: Session):
        subquery = (select(Module.fk_connectorid.label("connector_id"), func.count(Service.id).label("service_count"))
                    .outerjoin(Service, Module.id == Service.fk_moduleid).group_by(Module.fk_connectorid)).subquery()

        # coalesce is required (coalesce returns the first non-null value in a list)
        stmt = select(Connector, func.coalesce(subquery.c.service_count, 0).label("service_count")).outerjoin(subquery, subquery.c.connector_id == Connector.id)
        rows = db.execute(stmt).all()
        list_of_rows = []
        for row in rows:
            row[0].service_count = row.service_count
            list_of_rows.append(row[0])
        return list_of_rows


crud_connector = CRUDConnector(Connector)


class CRUDModule(CRUDBase):
    @staticmethod
    def get_all_module_ids_for_connector(db, connector_id):
        stmt = select(Module.id).where(Module.fk_connectorid == connector_id)
        return db.scalars(stmt).all()


crud_module = CRUDModule(Module)


class CRUDModuleParameter(CRUDBase):
    pass


crud_module_parameter = CRUDModuleParameter(ModuleParameter)