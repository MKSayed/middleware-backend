from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, SmallInteger, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import Base
from models.models_service import Service


class Module(Base):
    __tablename__ = "MODULE"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column("NAME", String(15), nullable=False)
    status: Mapped[str] = mapped_column("STATUS", String(1), nullable=False)
    description: Mapped[str] = mapped_column("DESCRIPTION", String(500))
    created: Mapped[Optional[datetime]] = mapped_column(
        "CREATED", server_default=func.current_timestamp()
    )
    updated: Mapped[Optional[datetime]] = mapped_column(
        "UPDATED", server_onupdate=func.current_timestamp()
    )
    fk_connectorid: Mapped[Optional[int]] = mapped_column(
        "FK_CONNECTORID", ForeignKey("CONNECTOR.ID"), index=True
    )
    module_params: Mapped[List["ModuleParameter"] | None] = relationship()

    @staticmethod
    async def get_all_module_ids_for_connector(db: AsyncSession, connector_id):
        stmt = select(Module.id).where(Module.fk_connectorid == connector_id)
        result = await db.scalars(stmt)
        return result.all()


class ModuleParameter(Base):
    __tablename__ = "MODULE_PARAMETER"
    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    key: Mapped[str] = mapped_column("KEY")
    value: Mapped[str] = mapped_column("VALUE")
    description: Mapped[str] = mapped_column("DESCRIPTION", String(500))
    created: Mapped[Optional[datetime]] = mapped_column(
        "CREATED", server_default=func.current_timestamp()
    )
    updated: Mapped[Optional[datetime]] = mapped_column(
        "UPDATED", server_onupdate=func.current_timestamp()
    )
    fk_moduleid: Mapped[int] = mapped_column(
        "FK_MODULEID", ForeignKey("MODULE.ID"), index=True
    )


class Connector(Base):
    __tablename__ = "CONNECTOR"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column("NAME", String(15), nullable=False)
    status: Mapped[str] = mapped_column("STATUS", String(1), nullable=False)
    created: Mapped[Optional[datetime]] = mapped_column(
        "CREATED", server_default=func.current_timestamp()
    )
    updated: Mapped[Optional[datetime]] = mapped_column(
        "UPDATED", server_onupdate=func.current_timestamp()
    )

    @staticmethod
    async def get_all_with_service_count(db: AsyncSession):
        subquery = (
            select(
                Module.fk_connectorid.label("connector_id"),
                func.count(Service.id).label("service_count"),
            )
            .outerjoin(Service, Module.id == Service.fk_moduleid)
            .group_by(Module.fk_connectorid)
        ).subquery()

        # coalesce is required (coalesce returns the first non-null value in a list)
        stmt = select(
            Connector, func.coalesce(subquery.c.service_count, 0).label("service_count")
        ).outerjoin(subquery, subquery.c.connector_id == Connector.id)
        result = await db.execute(stmt)
        result = result.all()
        list_of_rows = []
        for row in result:
            row[0].service_count = row.service_count
            list_of_rows.append(row[0])

        return list_of_rows
