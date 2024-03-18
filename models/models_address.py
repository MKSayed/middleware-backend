from typing import Optional

from sqlalchemy import (String, SmallInteger, ForeignKey)
from sqlalchemy.orm import Mapped, mapped_column


from core.database import Base


class Address(Base):
    __tablename__ = "ADDRESS"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column("NAME", String(35), nullable=False,
                                      comment="abbreviation for the place")
    details: Mapped[Optional[str]] = mapped_column("DETAILS", String(65))
    fk_police_staticd: Mapped[Optional[int]] = mapped_column("FK_POLICE_STATICD",
                                                             ForeignKey("POLICE_STATION.CD"), index=True)
    fk_areacd: Mapped[Optional[int]] = mapped_column("FK_AREACD", ForeignKey("AREA.CD"), index=True)
    fk_address_typecd: Mapped[Optional[int]] = mapped_column("FK_ADDRESS_TYPECD",
                                                             ForeignKey("ADDRESS_TYPE.CD"), index=True)
    __table_args__ = ({"comment": "Location of the kiosk device in the country"},)


class AddressType(Base):
    __tablename__ = "ADDRESS_TYPE"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True)
    descr: Mapped[str] = mapped_column("DESCR", String(30), nullable=False)


class Area(Base):
    __tablename__ = "AREA"

    cd: Mapped[int] = mapped_column("CD", primary_key=True)
    descr: Mapped[str] = mapped_column("DESCR", String(20), nullable=False)


class PoliceStation(Base):
    __tablename__ = "POLICE_STATION"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True)
    descr: Mapped[str] = mapped_column("DESCR", String(20), nullable=False)
