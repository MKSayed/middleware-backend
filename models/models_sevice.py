from datetime import date, datetime
from sqlalchemy import (String, SmallInteger, DECIMAL, PrimaryKeyConstraint, ForeignKey, CHAR, FetchedValue)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from core.database import Base


class Service(Base):
    __tablename__ = "SERVICE"

    id: Mapped[int] = mapped_column("ID", primary_key=True)
    ar_name: Mapped[str | None] = mapped_column("AR_NAME", String(40))
    eng_name: Mapped[str | None] = mapped_column("ENG_NAME", String(40))
    fk_moduleid: Mapped[int | None] = mapped_column("FK_MODULEID",
                                                       ForeignKey("MODULE.ID"), index=True)
    # looks like this column was added by mistake
    # fk_serviceid: Mapped[str | None] = mapped_column("FK_SERVICEID", String(5))
    fk_service_grouno: Mapped[int | None] = mapped_column("FK_SERVICE_GROUNO",
                                                             ForeignKey("SERVICE_GROUP.NO"), index=True)
    fk_providerid: Mapped[int | None] = mapped_column("FK_PROVIDERID",
                                                         ForeignKey("PROVIDER.ID"), index=True)


class ServiceCharge(Base):
    __tablename__ = "SERVICE_CHARGE"

    cd: Mapped[int] = mapped_column("CD", primary_key=True)
    descr: Mapped[str] = mapped_column("DESCR", String(50), nullable=False)
    value: Mapped[float] = mapped_column("VALUE", DECIMAL(9, 2), nullable=False)
    from_value: Mapped[float] = mapped_column("FROM", DECIMAL(9, 2), nullable=False)
    to_value: Mapped[float] = mapped_column("TO", DECIMAL(9, 2), nullable=False)
    active_dt: Mapped[date | None] = mapped_column("ACTIVE_DT",)
    slap: Mapped[float] = mapped_column("SLAP", DECIMAL(9, 2), nullable=False)
    fk_commission_tcd: Mapped[int | None] = mapped_column("FK_COMMISSION_TCD",
                                                             ForeignKey("COMMISSION_TYPE.CD"), index=True)
    fk_commission_vcd: Mapped[int | None] = mapped_column("FK_COMMISSION_VCD",
                                                             ForeignKey("COMMISSION_VALUE_TYPE.CD"), index=True)


class ServiceGroup(Base):
    __tablename__ = "SERVICE_GROUP"

    no: Mapped[int] = mapped_column("NO", SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column("NAME", String(45), nullable=False)


class ServiceParameter(Base):
    __tablename__ = "SERVICE_PARAMETER"

    ser: Mapped[int] = mapped_column("SER", SmallInteger, primary_key=True)
    service_value: Mapped[str] = mapped_column("SERVICE_VALUE", String(200), nullable=False)
    fk_serviceid: Mapped[str] = mapped_column("FK_SERVICEID", ForeignKey("SERVICE.ID"),
                                              nullable=False, index=True)
    fk_service_paracd: Mapped[int | None] = mapped_column("FK_SERVICE_PARACD",
                                                             ForeignKey("SERVICE_PARAMETER_TYPE.CD"), index=True)


class ServiceParameterType(Base):
    __tablename__ = "SERVICE_PARAMETER_TYPE"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True)
    descr: Mapped[str | None] = mapped_column("DESCR", String(35))
    constancy: Mapped[str | None] = mapped_column("CONSTANCY", String(1))
    direction: Mapped[str | None] = mapped_column("DIRECTION", String(1))


class ServicePrice(Base):
    __tablename__ = "SERVICE_PRICE"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    stdt: Mapped[date] = mapped_column("STDT", nullable=False)
    enddt: Mapped[date | None] = mapped_column("ENDDT",)
    price_value: Mapped[float] = mapped_column("PRICE_VALUE", DECIMAL(6, 2), nullable=False)
    max_value: Mapped[float | None] = mapped_column("MAX_VALUE", DECIMAL(6, 2))
    type: Mapped[str | None] = mapped_column("TYPE", String(8))
    list_value: Mapped[str | None] = mapped_column("LIST_VALUE", String(36))
    fk_serviceid: Mapped[str | None] = mapped_column("FK_SERVICEID", ForeignKey("SERVICE.ID"), index=True)
    fk_currencyid: Mapped[int | None] = mapped_column("FK_CURRENCYID", ForeignKey("CURRENCY.ID"), index=True)


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
    active_from: Mapped[datetime | None] = mapped_column("ACTIVE_FROM",)
    rate: Mapped[float] = mapped_column("RATE", DECIMAL(7, 2), nullable=False)
