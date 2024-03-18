from datetime import date
from typing import Optional, List

from sqlalchemy import (String, SmallInteger, PrimaryKeyConstraint, ForeignKey, CHAR, FetchedValue, Numeric)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.database import Base


class CommissionGroup(Base):
    __tablename__ = "COMMISSION_GROUP"

    cd: Mapped[int] = mapped_column("CD", primary_key=True)
    descr: Mapped[str] = mapped_column("DESCR", String(50), nullable=False)
    value: Mapped[float] = mapped_column("VALUE", Numeric(9, 2), nullable=False)
    from_value: Mapped[float] = mapped_column("FROM_VALUE", Numeric(9, 2), nullable=False)
    to_value: Mapped[float] = mapped_column("TO_VALUE", Numeric(9, 2), nullable=False)
    active_dt: Mapped[Optional[date]] = mapped_column("ACTIVE_DT")
    slap: Mapped[float] = mapped_column("SLAP", Numeric(9, 2), nullable=False)
    fk_commission_tcd: Mapped[Optional[int]] = mapped_column("FK_COMMISSION_TCD",
                                                             ForeignKey("COMMISSION_TYPE.CD"), index=True)
    fk_commission_vcd: Mapped[Optional[int]] = mapped_column("FK_COMMISSION_VCD",
                                                             ForeignKey("COMMISSION_VALUE_TYPE.CD"), index=True)
    fk_payment_typecd: Mapped[Optional[int]] = mapped_column("FK_PAYMENT_TYPECD",
                                                             ForeignKey("PAYMENT_TYPE.CD"), index=True)


class CommissionType(Base):
    __tablename__ = "COMMISSION_TYPE"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True)
    descr: Mapped[Optional[str]] = mapped_column("DESCR", String(35))
    creation_date: Mapped[Optional[date]] = mapped_column("CREATION_DATE",
                                                          server_default=func.current_date())


class CommissionValueType(Base):
    __tablename__ = "COMMISSION_VALUE_TYPE"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True)
    descr: Mapped[str] = mapped_column("DESCR", String(20), nullable=False)


class PaymentType(Base):
    __tablename__ = "PAYMENT_TYPE"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True)
    descr: Mapped[str] = mapped_column("DESCR", String(30), nullable=False)

