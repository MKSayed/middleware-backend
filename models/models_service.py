from datetime import date, datetime
from typing import Any

from sqlalchemy import String, SmallInteger, DECIMAL, ForeignKey, func, select, Identity, Enum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import get_sync_db
from models.base import Base
from models.models_connector import ModuleParameter


class KioskService(Base):
    __tablename__ = "KIOSK_SERVICE"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True, index=True)
    ar_name: Mapped[str | None] = mapped_column("AR_NAME", String(40))
    eng_name: Mapped[str] = mapped_column("ENG_NAME", String(40))


class KioskServiceFlow(Base):
    __tablename__ = "KIOSK_SERVICE_FLOW"

    fk_kiosk_service_cd: Mapped[Any] = mapped_column(
        "FK_KIOSK_SERVICE_CD",
        ForeignKey("KIOSK_SERVICE.CD"),
        primary_key=True,
        index=True,
    )
    fk_service_id: Mapped[Any] = mapped_column(
        "FK_SERVICE_ID", ForeignKey("SERVICE.ID"), index=True
    )
    order: Mapped[int] = mapped_column("ORDER", SmallInteger, primary_key=True)


class Service(AsyncAttrs, Base):
    __tablename__ = "SERVICE"

    id: Mapped[Any] = mapped_column("ID", SmallInteger, primary_key=True, index=True)
    ar_name: Mapped[str | None] = mapped_column("AR_NAME", String(40))
    eng_name: Mapped[str | None] = mapped_column("ENG_NAME", String(40))
    fk_module_id: Mapped[Any | None] = mapped_column(
        "FK_MODULE_ID", ForeignKey("MODULE.ID"), index=True, nullable=True
    )
    http_method: Mapped[str] = mapped_column("HTTP_METHOD", Enum('GET', 'POST', 'PUT', 'DELETE', 'PATCH', name="http_method_enum"))
    endpoint_path: Mapped[str] = mapped_column("ENDPOINT_PATH")
    # A service can depend on another server.
    # fk_service_id: Mapped[int | None] = mapped_column("FK_SERVICE_ID", ForeignKey("SERVICE.ID"), index=True)
    fk_provider_id: Mapped[Any | None] = mapped_column(
        "FK_PROVIDER_ID", ForeignKey("PROVIDER.ID"), index=True, nullable=True
    )
    # Relationships
    service_parameters: Mapped[list["ServiceParameter"]] = relationship(lazy="select")
    provider: Mapped["Provider"] = relationship(lazy="select")
    service_price: Mapped["ServicePrice"] = relationship(lazy="select")
    service_groups: Mapped[list["ServiceGroup"]] = relationship(
        secondary="SERVICE_SERVICEGROUP",
        back_populates="services",
        lazy="select",
    )


class ServiceGroup(Base):
    __tablename__ = "SERVICE_GROUP"

    no: Mapped[int] = mapped_column("NO", SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column("NAME", String(45), nullable=False)

    # Relationships
    services: Mapped[list["Service"]] = relationship(
        secondary="SERVICE_SERVICEGROUP",
        back_populates="service_groups",
        lazy="select",
    )


class ServiceServiceGroupAssociation(Base):
    __tablename__ = "SERVICE_SERVICEGROUP"

    # Compose a composite primary key by passing True as primary_key value for both columns
    fk_service_id: Mapped[Any] = mapped_column(
        "FK_SERVICE_ID", ForeignKey("SERVICE.ID"), primary_key=True, index=True
    )
    fk_service_group_no: Mapped[Any] = mapped_column(
        "FK_SERVICE_GROUP_NO",
        ForeignKey("SERVICE_GROUP.NO"),
        index=True,
        primary_key=True,
    )


class ServiceParameter(AsyncAttrs, Base):
    __tablename__ = "SERVICE_PARAMETER"

    id: Mapped[int] = mapped_column(
        "ID", Identity(start=30000, increment=1), primary_key=True,
        comment= "service_parameter ids starts from 30000 to distinguish it from module_parameters which starts at 0"
    )
    key: Mapped[str] = mapped_column("KEY", String(200), nullable=False)
    value: Mapped[str | None] = mapped_column("VALUE")
    parent_id: Mapped[int | None] = mapped_column(
        "PARENT_ID", comment="This could refer to a service_parameter_id or module_parameter_id")
    fk_service_id: Mapped[int] = mapped_column(
        "FK_SERVICE_ID", ForeignKey("SERVICE.ID"), nullable=False, index=True
    )
    # fk_service_para_type_cd: Mapped[int | None] = mapped_column(
    #     "FK_SERVICE_PARA_TYPE_CD", ForeignKey("SERVICE_PARAMETER_TYPE.CD"), index=True
    # )
    fk_param_type_cd: Mapped[Any] = mapped_column("FK_PARAM_TYPE_CD", ForeignKey("PARAM_TYPE.CD"), index=True)
    fk_param_loc_cd: Mapped[Any] = mapped_column("FK_PARAM_LOC_CD", ForeignKey("PARAM_LOC.CD"), index=True)
    is_optional: Mapped[bool] = mapped_column("IS_OPTIONAL")
    is_client: Mapped[bool] = mapped_column("IS_CLIENT")
    nest_level: Mapped[int] = mapped_column(
        "NEST_LEVEL",
        default=lambda context: ServiceParameter.on_insert(context),
        onupdate=lambda context: ServiceParameter.on_update(context),
    )
    value_reference_id: Mapped[int | None] = mapped_column("VALUE_REFERENCE_ID",
                                                        comment="This could refer to a service_parameter_id or module_parameter_id")

    # parent_param: Mapped["ServiceParameter"] = relationship(
    #     "ServiceParameter", back_populates="children", remote_side=[ser], lazy="select"
    # )
    # children: Mapped[list["ServiceParameter"]] = relationship(
    #     "ServiceParameter", back_populates="parent_param"
    # )
    type:  Mapped["ParamType"] = relationship(lazy="selectin")

    @staticmethod
    def on_insert(context):
        parent_id = context.get_current_parameters().get("PARENT_ID", None)
        if not parent_id:
            return 0

        for db in get_sync_db():
            stmt = select(ServiceParameter).filter_by(id=parent_id)
            parent = db.execute(stmt).scalars().first()
            # If the parent is not found in the database, then its parent is a module parameter
            if parent is None:
                stmt = select(ModuleParameter).filter_by(id=parent_id)
                parent = db.execute(stmt).scalars().first()

            return parent.nest_level + 1

    @staticmethod
    def on_update(context):
        # TODO handle the case when a parameter nest level is changed it also change
        # all it's children's nest level
        parent_id = context.get_current_parameters().get("PARENT_ID", None)
        for db in get_sync_db():
            # Do not update the nest_level if the parent hasn't changed
            if not parent_id:
                stmt = select(ServiceParameter).filter_by(
                    id=context.get_current_parameters().get(
                        "SERVICE_PARAMETER_ID", None
                    )
                )
                service_parameter = db.execute(stmt).scalars().first()
                # return the same nest level if the parent hasn't changed
                return service_parameter.nest_level

            stmt = select(ServiceParameter).filter_by(id=parent_id)
            parent = db.execute(stmt).scalars().first()
            # If the parent is not found in the database, then its parent is a module parameter
            if parent is None:
                stmt = select(ModuleParameter).filter_by(id=parent_id)
                parent = db.execute(stmt).scalars().first()
            return parent.nest_level + 1


class ServiceCharge(Base):
    __tablename__ = "SERVICE_CHARGE"

    cd: Mapped[int] = mapped_column("CD", primary_key=True, index=True)
    descr: Mapped[str] = mapped_column("DESCR", String(50), nullable=False)
    value: Mapped[float] = mapped_column("VALUE", DECIMAL(9, 2), nullable=False)
    from_value: Mapped[float] = mapped_column("FROM", DECIMAL(9, 2), nullable=False)
    to_value: Mapped[float] = mapped_column("TO", DECIMAL(9, 2), nullable=False)
    active_dt: Mapped[date | None] = mapped_column(
        "ACTIVE_DT",
    )
    slap: Mapped[float] = mapped_column("SLAP", DECIMAL(9, 2), nullable=False)
    fk_commission_tcd: Mapped[int | None] = mapped_column(
        "FK_COMMISSION_TCD", ForeignKey("COMMISSION_TYPE.CD"), index=True
    )
    fk_commission_vcd: Mapped[int | None] = mapped_column(
        "FK_COMMISSION_VCD", ForeignKey("COMMISSION_VALUE_TYPE.CD"), index=True
    )


# class ServiceParameterType(Base):
#     __tablename__ = "SERVICE_PARAMETER_TYPE"
#
#     cd: Mapped[int] = mapped_column(
#         "CD",
#         SmallInteger,
#         primary_key=True,
#         comment="1 body input 2 body output 3 input header",
#     )
#     descr: Mapped[str | None] = mapped_column("DESCR", String(35))
#     # constancy: Mapped[str | None] = mapped_column("CONSTANCY", String(1), comment="1 Variable 2 Constant")
#     direction: Mapped[str | None] = mapped_column(
#         "DIRECTION", String(1), comment="1 input 2 output"
#     )


class ParamType(Base):
    __tablename__ = "PARAM_TYPE"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True)
    descr: Mapped[str] = mapped_column("DESCR", String(35), nullable=False)


class ParamLoc(Base):
    __tablename__ = "PARAM_LOC"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True)
    descr: Mapped[str] = mapped_column("DESCR", String(35), nullable=False)


class ServicePrice(Base):
    __tablename__ = "SERVICE_PRICE"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    stdt: Mapped[date] = mapped_column(
        "STDT", nullable=False, server_default=func.current_date()
    )
    enddt: Mapped[date | None] = mapped_column("ENDDT")
    price_value: Mapped[float] = mapped_column(
        "PRICE_VALUE", DECIMAL(6, 2)
    )
    max_value: Mapped[float | None] = mapped_column("MAX_VALUE", DECIMAL(6, 2))
    type: Mapped[str] = mapped_column("TYPE", Enum('FIXED', 'RANGE', 'LIST', name='price_type_enum'))
    # list_value: Mapped[str | None] = mapped_column("LIST_VALUE", String(36))
    fk_service_id: Mapped[Any] = mapped_column(
        "FK_SERVICE_ID", ForeignKey("SERVICE.ID"), index=True
    )
    fk_currency_id: Mapped[Any] = mapped_column(
        "FK_CURRENCY_ID",
        ForeignKey("CURRENCY.ID"),
        index=True,
        # Todo to be changed later when the application start supporting multiple currencies
        default="1",
    )


class PriceList(Base):
    __tablename__ = "PRICE_LIST"
    id: Mapped[int] = mapped_column("ID", primary_key=True)
    key: Mapped[str] = mapped_column("KEY", String(40))
    price_value: Mapped[float] = mapped_column("PRICE_VALUE", DECIMAL(6, 2))
    fk_service_price_id: Mapped[Any] = mapped_column("FK_SERVICE_PRICE_ID", ForeignKey("SERVICE_PRICE.ID"), index=True)


class Provider(Base):
    __tablename__ = "PROVIDER"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    ar_name: Mapped[str] = mapped_column("AR_NAME", String(40), nullable=False)
    eng_name: Mapped[str] = mapped_column("ENG_NAME", String(40), nullable=False)


class Currency(Base):
    __tablename__ = "CURRENCY"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    code: Mapped[str] = mapped_column("CODE", String(5), nullable=False)
    name: Mapped[str | None] = mapped_column("NAME", String(20))
    active_from: Mapped[datetime | None] = mapped_column(
        "ACTIVE_FROM",
    )
    rate: Mapped[float] = mapped_column("RATE", DECIMAL(7, 2), nullable=False)
