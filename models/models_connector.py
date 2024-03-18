from datetime import date, time
from typing import Optional, List

from sqlalchemy import (String, SmallInteger, PrimaryKeyConstraint, ForeignKey, CHAR, FetchedValue)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.database import Base


class Module(Base):
    __tablename__ = "MODULE"

    ser: Mapped[int] = mapped_column("SER", SmallInteger, primary_key=True)
    destination: Mapped[Optional[str]] = mapped_column("DESTINATION", String(25))
    time_out: Mapped[Optional[time]] = mapped_column("TIME_OUT")
    deviceid: Mapped[Optional[str]] = mapped_column("DEVICEID", String(10))
    target_url: Mapped[Optional[str]] = mapped_column("TARGET_URL", String(40))
    organization_code: Mapped[Optional[str]] = mapped_column("ORGANIZATION_CODE", String(6))
    fk_connectorid: Mapped[Optional[int]] = mapped_column("FK_CONNECTORID",
                                                          ForeignKey("CONNECTOR.ID"), index=True)


class Connector(Base):
    __tablename__ = "CONNECTOR"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column("NAME", String(15), nullable=False)
    status: Mapped[str] = mapped_column("STATUS", String(1), nullable=False)
    creation_date: Mapped[Optional[date]] = mapped_column("CREATION_DATE",
                                                          server_default=func.current_date())
    updated_date: Mapped[Optional[date]] = mapped_column("UPDATED_DATE",
                                                         server_onupdate=func.current_date())