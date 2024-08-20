from datetime import datetime
from typing import Optional, List
import asyncio

from fastapi import Depends
from sqlalchemy import String, SmallInteger, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs

from core.database import get_sync_db
from models.base import Base


class Module(Base):
    __tablename__ = "MODULE"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column("NAME", String(15), nullable=False)
    status: Mapped[str] = mapped_column("STATUS", String(1), nullable=False)
    description: Mapped[str] = mapped_column("DESCRIPTION", String(500))
    base_url: Mapped[str] = mapped_column("BASE_URL")
    timeout: Mapped[int | None] = mapped_column("TIMEOUT")
    created: Mapped[Optional[datetime]] = mapped_column(
        "CREATED", server_default=func.current_timestamp()
    )
    updated: Mapped[Optional[datetime]] = mapped_column(
        "UPDATED", server_onupdate=func.current_timestamp()
    )
    fk_connector_id: Mapped[int | None] = mapped_column(
        "FK_CONNECTOR_ID", ForeignKey("CONNECTOR.ID"), index=True
    )
    is_xml: Mapped[bool] = mapped_column("IS_XML")

    # Relationships
    module_params: Mapped[List["ModuleParameter"] | None] = relationship(lazy="select")

    @staticmethod
    async def get_all_module_ids_for_connector(db: AsyncSession, connector_id):
        stmt = select(Module.id).where(Module.fk_connector_id == connector_id)
        result = await db.scalars(stmt)
        return result.all()


class ModuleParameter(AsyncAttrs, Base):
    __tablename__ = "MODULE_PARAMETER"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    key: Mapped[str] = mapped_column("KEY", String(200))
    value: Mapped[str | None] = mapped_column("VALUE")
    description: Mapped[str] = mapped_column("DESCRIPTION", String(500))
    parent_id: Mapped[int | None] = mapped_column("PARENT_ID", ForeignKey("MODULE_PARAMETER.ID"))
    fk_param_type_cd: Mapped[int] = mapped_column("FK_PARAM_TYPE_CD", ForeignKey("PARAM_TYPE.CD"), index=True)
    fk_param_loc_cd: Mapped[int | None] = mapped_column("FK_PARAM_LOC_CD", ForeignKey("PARAM_LOC.CD"), index=True)
    # created: Mapped[Optional[datetime]] = mapped_column(
    #     "CREATED", server_default=func.current_timestamp()
    # )
    # updated: Mapped[Optional[datetime]] = mapped_column(
    #     "UPDATED", server_onupdate=func.current_timestamp()
    # )
    fk_module_id: Mapped[int] = mapped_column(
        "FK_MODULE_ID", ForeignKey("MODULE.ID"), index=True
    )
    nest_level: Mapped[int] = mapped_column("NEST_LEVEL", default=lambda context: ModuleParameter.on_insert(context), onupdate=lambda context: ModuleParameter.on_update(context))
    is_optional: Mapped[bool] = mapped_column("IS_OPTIONAL")
    is_client: Mapped[bool] = mapped_column("IS_CLIENT")
    value_reference_id: Mapped[int | None] = mapped_column("VALUE_REFERENCE_ID",
                                                        comment="This could refer to a service_parameter_id or module_parameter_id")
    # Relationships
    parent_param: Mapped["ModuleParameter"] = relationship("ModuleParameter", remote_side=[id])
    type = relationship("ParamType", lazy="selectin")
    location = relationship("ParamLoc")

    @staticmethod
    def on_insert(context):
        parent_id = context.get_current_parameters().get("PARENT_ID", None)
        if not parent_id:
            return 0

        for db in get_sync_db():
            stmt = select(ModuleParameter).filter_by(id=parent_id)
            parent = db.execute(stmt).scalars().first()

            return parent.nest_level + 1

    @staticmethod
    def on_update(context):
        parent_id = context.get_current_parameters().get("PARENT_ID", None)
        for db in get_sync_db():
            # Do not update the nest_level if the parent hasn't changed
            if not parent_id:
                stmt = select(ModuleParameter).filter_by(
                    id=context.get_current_parameters().get("MODULE_PARAMETER_ID", None))
                module = db.execute(stmt).scalars().first()
                # return the same nest level if the parent hasn't changed
                return module.nest_level

            stmt = select(ModuleParameter).filter_by(id=parent_id)
            parent = db.execute(stmt).scalars().first()
            return parent.nest_level + 1


class Connector(Base):
    __tablename__ = "CONNECTOR"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column("NAME", String(15), nullable=False)
    status: Mapped[str] = mapped_column("STATUS", String(1), nullable=False)
    created: Mapped[datetime | None] = mapped_column(
        "CREATED", server_default=func.current_timestamp()
    )
    updated: Mapped[datetime | None] = mapped_column(
        "UPDATED", server_onupdate=func.current_timestamp()
    )

    @staticmethod
    async def get_all_with_service_count(db: AsyncSession):
        # Import inside the method to prevent circular imports
        from models.models_service import Service
        subquery = (
            select(
                Module.fk_connector_id.label("connector_id"),
                func.count(Service.id).label("service_count"),
            )
            .outerjoin(Service, Module.id == Service.fk_module_id)
            .group_by(Module.fk_connector_id)
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
