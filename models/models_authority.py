from datetime import date
from typing import Optional

from sqlalchemy import (String, SmallInteger, PrimaryKeyConstraint, ForeignKey, CHAR)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from core.database import Base


class Application(Base):
    __tablename__ = 'APPLICATION'

    num: Mapped[int] = mapped_column("NUM", SmallInteger, primary_key=True, index=True, autoincrement=False)
    name: Mapped[str] = mapped_column("NAME", String(30))


class Permission(Base):
    __tablename__ = "PERMISSION"

    number: Mapped[int] = mapped_column("NUMBER", primary_key=True, index=True, autoincrement=False)
    name: Mapped[str] = mapped_column("NAME", String(20))
    active: Mapped[str] = mapped_column("ACTIVE", CHAR(3))
    expiry_date: Mapped[Optional[date]] = mapped_column("EXPIRY_DATE")
    creation_date: Mapped[date] = mapped_column("CREATION_DATE", server_default=func.current_date())
    fk_applicationnum: Mapped[int] = mapped_column("FK_APPLICATIONNUM", ForeignKey('APPLICATION.NUM'),
                                                   index=True)


class Authority(Base):
    __tablename__ = "AUTHORITY"

    serial: Mapped[int] = mapped_column("SERIAL")
    start_date: Mapped[date] = mapped_column("START_DATE")
    end_date: Mapped[Optional[date]] = mapped_column("END_DATE")
    active: Mapped[Optional[str]] = mapped_column("ACTIVE", CHAR(1))
    fk_permission_number: Mapped[int] = mapped_column("FK_PERMISSION_NUMBER",
                                                      ForeignKey("PERMISSION.NUMBER"), index=True)
    fk_authorized_rnumber: Mapped[int] = mapped_column("FK_AUTHORIZED_RNUMBER",
                                                       ForeignKey("AUTHORIZED_ROLE.NUMBER"), index=True)

    __table_args__ = (
        PrimaryKeyConstraint("FK_PERMISSION_NUMBER", "FK_AUTHORIZED_RNUMBER"),)


class AuthorizedRole(Base):
    __tablename__ = "AUTHORIZED_ROLE"

    number: Mapped[int] = mapped_column("NUMBER", SmallInteger, primary_key=True, autoincrement=False)
    name: Mapped[Optional[str]] = mapped_column("NAME", String(50))
    creation_date: Mapped[Optional[date]] = mapped_column("CREATION_DATE", server_default=func.current_date())
    expiry_date: Mapped[Optional[date]] = mapped_column("EXPIRY_DATE")


class AssignedRole(Base):
    __tablename__ = "ASSIGNED_ROLE"

    active: Mapped[Optional[str]] = mapped_column("ACTIVE", CHAR(1))
    creation_date: Mapped[date] = mapped_column("CREATION_DATE")
    fk_authorized_rnumber: Mapped[int] = mapped_column("FK_AUTHORIZED_RNUMBER",
                                                       ForeignKey("AUTHORIZED_ROLE.NUMBER"), index=True)
    fk_userid: Mapped[int] = mapped_column("FK_USERID", ForeignKey("USER.ID"), index=True)

    __table_args__ = (PrimaryKeyConstraint("FK_AUTHORIZED_RNUMBER", "FK_USERID"),)
