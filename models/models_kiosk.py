from sqlalchemy import Integer, Numeric, String, SmallInteger, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from models.base import Base
from datetime import datetime


class Kiosk(Base):
    __tablename__ = "KIOSK"

    id: Mapped[int] = mapped_column("ID", Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        "USERNAME", String(25), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column("PASSWORD", String(72), nullable=False)
    account_no: Mapped[Numeric] = mapped_column(
        "ACCOUNT_NO", Numeric(10), nullable=False
    )
    ar_name: Mapped[str] = mapped_column("AR_NAME", String(40), nullable=False)
    eng_name: Mapped[str] = mapped_column("ENG_NAME", String(40), nullable=False)
    descr: Mapped[Optional[str]] = mapped_column("DESCR", String(100))
    creation_date: Mapped[datetime] = mapped_column(
        "CREATION_DATE", server_default=func.current_timestamp()
    )
    updated_date: Mapped[datetime | None] = mapped_column(
        "UPDATED_DATE", server_onupdate=func.current_timestamp()
    )
    status: Mapped[Optional[str]] = mapped_column("STATUS", String(1))
    deleted_flag: Mapped[Optional[int]] = mapped_column("DELETED_FLAG", SmallInteger)
    cd_part1: Mapped[Optional[int]] = mapped_column("CD_PART1", SmallInteger)
    cd_part2: Mapped[Optional[int]] = mapped_column("CD_PART2", SmallInteger)
    commission_check: Mapped[Optional[str]] = mapped_column(
        "COMMISSION_CHECK", String(1)
    )
    service_group_check: Mapped[Optional[str]] = mapped_column(
        "SERVICE_GROUP_CHECK", String(1)
    )
    service_charge_check: Mapped[Optional[str]] = mapped_column(
        "SERVICE_CHARGE_CHECK", String(1)
    )
    fk_service_grouno: Mapped[Optional[int]] = mapped_column(
        "FK_SERVICE_GROUNO", SmallInteger, ForeignKey("SERVICE_GROUP.NO"), index=True
    )
    fk_addressid: Mapped[Optional[int]] = mapped_column(
        "FK_ADDRESSID", ForeignKey("ADDRESS.ID"), index=True
    )
    fk_kiosk_familyid: Mapped[Optional[int]] = mapped_column(
        "FK_KIOSK_FAMILYID", ForeignKey("KIOSK_FAMILY.ID"), index=True
    )
    fk_commission_gcd: Mapped[Optional[int]] = mapped_column(
        "FK_COMMISSION_GCD", ForeignKey("COMMISSION_GROUP.CD"), index=True
    )


class KioskFamily(Base):
    __tablename__ = "KIOSK_FAMILY"

    id: Mapped[int] = mapped_column("ID", Integer, primary_key=True)
    account_no: Mapped[Numeric] = mapped_column(
        "ACCOUNT_NO", Numeric(10), nullable=False
    )
    ar_name: Mapped[str] = mapped_column("AR_NAME", String(40), nullable=False)
    eng_name: Mapped[str] = mapped_column("ENG_NAME", String(40), nullable=False)
    type: Mapped[Optional[str]] = mapped_column("TYPE", String(1))
    descr: Mapped[Optional[str]] = mapped_column("DESCR", String(100))
    updated_date: Mapped[Optional[datetime]] = mapped_column(
        "UPDATED_DATE", server_onupdate=func.current_timestamp()
    )
    status: Mapped[Optional[str]] = mapped_column("STATUS", String(1))
    deleted_flag: Mapped[Optional[int]] = mapped_column("DELETED_FLAG", SmallInteger)
    fk_commission_gcd: Mapped[Optional[int]] = mapped_column(
        "FK_COMMISSION_GCD", ForeignKey("COMMISSION_GROUP.CD"), index=True
    )
    fk_service_charcd: Mapped[Optional[int]] = mapped_column(
        "FK_SERVICE_CHARCD", ForeignKey("SERVICE_CHARGE.CD"), index=True
    )
    fk_service_grouno: Mapped[Optional[int]] = mapped_column(
        "FK_SERVICE_GROUNO", ForeignKey("SERVICE_GROUP.NO"), index=True
    )
    # looks like this next column is present here by mistake
    # fk_kiosk_familyid: Mapped[Optional[int]] = mapped_column("FK_KIOSK_FAMILYID", Integer)


class KioskOperatorLog(Base):
    __tablename__ = "KIOSK_OPERATOR_LOG"

    id: Mapped[Numeric] = mapped_column("ID", Numeric(14), primary_key=True)
    ip_address: Mapped[Optional[str]] = mapped_column("IP_ADDRESS", String(15))
    entrystamp: Mapped[Optional[datetime]] = mapped_column(
        "ENTRYSTAMP", server_default=func.current_timestamp()
    )
    aff_field: Mapped[Numeric] = mapped_column("AFF_FIELD", Numeric(10), nullable=False)
    aff_field2: Mapped[Optional[Numeric]] = mapped_column("AFF_FIELD2", Numeric(10))
    type: Mapped[Optional[str]] = mapped_column("TYPE", String(1))
    fk_kioskid: Mapped[Optional[int]] = mapped_column(
        "FK_KIOSKID", Integer, ForeignKey("KIOSK.ID"), index=True
    )
    fk_permission_number: Mapped[Optional[int]] = mapped_column(
        "FK_PERMISSION_NUMBER", ForeignKey("PERMISSION.NUMBER"), index=True
    )


class KioskType(Base):
    __tablename__ = "KIOSK_TYPE"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    descr: Mapped[str] = mapped_column("DESCR", String(30), nullable=False)
