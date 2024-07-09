from datetime import date, datetime
from typing import Any

from sqlalchemy import String, SmallInteger, DECIMAL, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from models.base import Base


class Service(AsyncAttrs, Base):
    __tablename__ = "SERVICE"

    id: Mapped[Any] = mapped_column("ID", SmallInteger, primary_key=True, index=True)
    ar_name: Mapped[str | None] = mapped_column("AR_NAME", String(40))
    eng_name: Mapped[str | None] = mapped_column("ENG_NAME", String(40))
    fk_moduleid: Mapped[Any | None] = mapped_column(
        "FK_MODULEID", ForeignKey("MODULE.ID"), index=True, nullable=True
    )
    # A service can depend on another server.
    # fk_serviceid: Mapped[int | None] = mapped_column("FK_SERVICEID", ForeignKey("SERVICE.ID"), index=True)
    fk_providerid: Mapped[Any | None] = mapped_column(
        "FK_PROVIDERID", ForeignKey("PROVIDER.ID"), index=True, nullable=True
    )
    # Relationships
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
    fk_serviceid: Mapped[Any] = mapped_column(
        "FK_SERVICEID", ForeignKey("SERVICE.ID"), primary_key=True, index=True
    )
    fk_service_grouno: Mapped[Any] = mapped_column(
        "FK_SERVICE_GROUNO",
        ForeignKey("SERVICE_GROUP.NO"),
        index=True,
        primary_key=True,
    )


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


class ServiceParameter(Base):
    __tablename__ = "SERVICE_PARAMETER"

    ser: Mapped[int] = mapped_column("SER", SmallInteger, primary_key=True)
    service_value: Mapped[str] = mapped_column(
        "SERVICE_VALUE", String(200), nullable=False
    )
    fk_serviceid: Mapped[int] = mapped_column(
        "FK_SERVICEID", ForeignKey("SERVICE.ID"), nullable=False, index=True
    )
    fk_service_para_typecd: Mapped[int | None] = mapped_column(
        "FK_SERVICE_PARA_TYPE_CD", ForeignKey("SERVICE_PARAMETER_TYPE.CD"), index=True
    )


class ServiceParameterType(Base):
    __tablename__ = "SERVICE_PARAMETER_TYPE"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True)
    descr: Mapped[str | None] = mapped_column("DESCR", String(35))
    constancy: Mapped[str | None] = mapped_column("CONSTANCY", String(1))
    direction: Mapped[str | None] = mapped_column("DIRECTION", String(1))


class ServicePrice(Base):
    __tablename__ = "SERVICE_PRICE"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    stdt: Mapped[date] = mapped_column(
        "STDT", nullable=False, server_default=func.current_date()
    )
    enddt: Mapped[date | None] = mapped_column("ENDDT")
    price_value: Mapped[float] = mapped_column(
        "PRICE_VALUE", DECIMAL(6, 2), nullable=False
    )
    max_value: Mapped[float | None] = mapped_column("MAX_VALUE", DECIMAL(6, 2))
    # Type = String "fixed" or "range"
    type: Mapped[str | None] = mapped_column("TYPE", String(8))
    list_value: Mapped[str | None] = mapped_column("LIST_VALUE", String(36))
    fk_serviceid: Mapped[Any] = mapped_column(
        "FK_SERVICEID", ForeignKey("SERVICE.ID"), index=True
    )
    fk_currencyid: Mapped[Any] = mapped_column(
        "FK_CURRENCYID",
        ForeignKey("CURRENCY.ID"),
        index=True,
        # Todo to be changed later when the application start supporting multiple currencies
        default="1",
    )


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
