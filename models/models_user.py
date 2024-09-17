from typing import Optional
from models.base import Base
from sqlalchemy import Numeric
from sqlalchemy import (
    String,
    SmallInteger,
    Date,
    Time,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    ForeignKey,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date, time


class UserType(Base):
    __tablename__ = "USER_TYPE"

    cd: Mapped[int] = mapped_column("CD", SmallInteger, primary_key=True, index=True)
    descr: Mapped[str] = mapped_column("DESCR", String(50), nullable=False)


class User(Base):
    __tablename__ = "USER"

    id: Mapped[int] = mapped_column("ID", primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        "USERNAME", String(25), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column("PASSWORD", String(72), nullable=False)
    name: Mapped[str] = mapped_column("NAME", String(60), nullable=False)
    national_id: Mapped[Optional[str]] = mapped_column("NATIONAL_ID", String(14))
    status: Mapped[str] = mapped_column("STATUS", String(7), nullable=False)
    # tax_id: Mapped[Optional[int]] = mapped_column("TAX_ID") Todo: what is that? :D
    fk_user_typecd: Mapped[int] = mapped_column(
        "FK_USER_TYPECD", ForeignKey("USER_TYPE.CD"), nullable=True, index=True
    )
    logs = relationship("UserLog", back_populates="user")


class UserLog(Base):
    __tablename__ = "USER_LOG"

    date: Mapped[date] = mapped_column("DATE", Date, nullable=False, index=True)
    time: Mapped[time] = mapped_column("TIME", Time, nullable=False, index=True)
    fk_userid: Mapped[int] = mapped_column(
        "FK_USERID", ForeignKey("USER.ID"), nullable=False, index=True
    )
    fk_permission_number: Mapped[Optional[int]] = mapped_column(
        "FK_PERMISSION_NUMBER", ForeignKey("PERMISSION.NUMBER"), index=True
    )
    user = relationship("User", back_populates="logs")

    __table_args__ = (PrimaryKeyConstraint("DATE", "TIME", "FK_USERID", name="idO"),)


class UserLogHistory(Base):
    __tablename__ = "USER_LOG_HISTORY"
    old_data: Mapped[Optional[str]] = mapped_column("OLD_DATA", String(35))
    aff_field: Mapped[Optional[str]] = mapped_column("AFF_FIELD", String(10))
    amount_paid: Mapped[Optional[float]] = mapped_column("AMOUNT_PAID", Numeric(8, 2))
    fk_user_logdate: Mapped[date] = mapped_column(
        "FK_USER_LOGDATE", Date, nullable=False, index=True
    )
    fk_user_logtime: Mapped[time] = mapped_column(
        "FK_USER_LOGTIME", Time, nullable=False, index=True
    )
    fk_user_logfk_userid: Mapped[int] = mapped_column(
        "FK_USER_LOGFK_USERID", nullable=False, index=True
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            "FK_USER_LOGDATE", "FK_USER_LOGTIME", "FK_USER_LOGFK_USERID", name="idP"
        ),
        ForeignKeyConstraint(
            ["FK_USER_LOGDATE", "FK_USER_LOGTIME", "FK_USER_LOGFK_USERID"],
            ["USER_LOG.DATE", "USER_LOG.TIME", "USER_LOG.FK_USERID"],
        ),
    )
