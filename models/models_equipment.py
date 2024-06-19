from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    String,
    SmallInteger,
    PrimaryKeyConstraint,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from core.database import Base


class AssignedEquipment(Base):
    __tablename__ = "ASSIGNED_EQUIPMENT"

    timestamp: Mapped[datetime] = mapped_column(
        "TIMESTAMP", nullable=False, server_default=func.current_timestamp()
    )
    start_date: Mapped[date] = mapped_column("START_DATE", nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(
        "END_DATE",
    )
    status: Mapped[Optional[int]] = mapped_column("STATUS", SmallInteger)
    fk_kioskid: Mapped[int] = mapped_column(
        "FK_KIOSKID", ForeignKey("KIOSK.ID"), nullable=False, index=True
    )
    fk_kiosk_equipmid: Mapped[int] = mapped_column(
        "FK_KIOSK_EQUIPMID",
        ForeignKey("KIOSK_EQUIPMENT.ID"),
        nullable=False,
        index=True,
    )

    __table_args__ = (
        PrimaryKeyConstraint("TIMESTAMP", "FK_KIOSKID", "FK_KIOSK_EQUIPMID"),
    )


class EquipmentType(Base):
    __tablename__ = "EQUIPMENT_TYPE"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True)
    descr: Mapped[Optional[str]] = mapped_column("DESCR", String(50))
    status: Mapped[Optional[int]] = mapped_column("STATUS", SmallInteger)


class KioskEquipment(Base):
    __tablename__ = "KIOSK_EQUIPMENT"

    id: Mapped[int] = mapped_column("ID", primary_key=True)
    descr: Mapped[Optional[str]] = mapped_column("DESCR", String(100))
    component_ser_num: Mapped[Optional[str]] = mapped_column(
        "COMPONENT_SER_NUM", String(20)
    )
    component_ip_address: Mapped[Optional[str]] = mapped_column(
        "COMPONENT_IP_ADDRESS", String(15)
    )
    creation_date: Mapped[Optional[datetime]] = mapped_column(
        "CREATION_DATE", server_default=func.current_timestamp()
    )
    status: Mapped[Optional[int]] = mapped_column("STATUS", SmallInteger)
    start_date: Mapped[Optional[date]] = mapped_column("START_DATE")
    end_date: Mapped[Optional[date]] = mapped_column("END_DATE")
    fk_equipment_tycd: Mapped[Optional[int]] = mapped_column(
        "FK_EQUIPMENT_TYCD", ForeignKey("EQUIPMENT_TYPE.CD"), index=True
    )
