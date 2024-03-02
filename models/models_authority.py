from database import Base
from datetime import date
from typing import Optional
from sqlalchemy import Column
from sqlalchemy import (Integer, String, SmallInteger, Date, PrimaryKeyConstraint, ForeignKey, CHAR)
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Application(Base):
    __tablename__ = 'APPLICATION'

    num: Mapped[int] = mapped_column("NUM", SmallInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column("NAME", String(30))


class TransactionKiosk(Base):
    __tablename__ = "TRANSACTION_KIOSK"

    number: Mapped[int] = mapped_column("NUMBER", primary_key=True, index=True)
    active: Mapped[str] = mapped_column("ACTIVE", CHAR(3))
    expiry_date: Mapped[date] = mapped_column("EXPIRY_DATE")
    creation_date: Mapped[date] = mapped_column("CREATION_DATE")
    fk_applicationnum: Mapped[int] = mapped_column("FK_APPLICATIONNUM", ForeignKey('APPLICATION.NUM'), index=True)


class Authority(Base):
    __tablename__ = "AUTHORITY"

    serial: Mapped[int] = mapped_column("SERIAL")
    start_date: Mapped[date] = mapped_column("START_DATE")
    end_date: Mapped[Optional[date]] = mapped_column("END_DATE")
    active: Mapped[Optional[str]] = mapped_column("ACTIVE", CHAR(1))
    fk_transaction_number: Mapped[int] = mapped_column("FK_TRANSACTION_NUMBER",
                                                       ForeignKey("TRANSACTION_KIOSK.NUMBER"), index=True)
    fk_authorized_rnumber: Mapped[int] = mapped_column("FK_AUTHORIZED_RNUMBER",
                                                       ForeignKey("AUTHORIZED_ROLE.NUMBER"), index=True)

    __table_args__ = (
        PrimaryKeyConstraint("FK_TRANSACTION_NUMBER", "FK_AUTHORIZED_RNUMBER"),)


class AuthorizedRole(Base):
    __tablename__ = "AUTHORIZED_ROLE"

    number: Mapped[int] = mapped_column("NUMBER", SmallInteger, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column("NAME", String(50))
    creation_date: Mapped[Optional[date]] = mapped_column("CREATION_DATE")
    expiry_date: Mapped[Optional[date]] = mapped_column("EXPIRY_DATE")


class AssignedRole(Base):
    __tablename__ = "ASSIGNED_ROLE"

    active: Mapped[Optional[str]] = mapped_column("ACTIVE", CHAR(1))
    creation_date: Mapped[date] = mapped_column("CREATION_DATE")
    fk_authorized_rnumber: Mapped[int] = mapped_column("FK_AUTHORIZED_RNUMBER",
                                                       ForeignKey("AUTHORIZED_ROLE.NUMBER"), index=True)
    fk_userid: Mapped[int] = mapped_column("FK_USERID", ForeignKey("USER.ID"), index=True)

    __table_args__ = (PrimaryKeyConstraint("FK_AUTHORIZED_RNUMBER", "FK_USERID"),)
