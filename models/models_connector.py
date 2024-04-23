from datetime import datetime
from typing import Optional, List

from sqlalchemy import (String, SmallInteger, ForeignKey)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.database import Base


class Module(Base):
    __tablename__ = "MODULE"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column("NAME", String(15), nullable=False)
    status: Mapped[str] = mapped_column("STATUS", String(1), nullable=False)
    description: Mapped[str] = mapped_column("DESCRIPTION", String(500))
    created: Mapped[Optional[datetime]] = mapped_column("CREATED",
                                                        default=func.current_timestamp())
    updated: Mapped[Optional[datetime]] = mapped_column("UPDATED",
                                                        onupdate=func.current_timestamp())
    fk_connectorid: Mapped[Optional[int]] = mapped_column("FK_CONNECTORID",
                                                          ForeignKey("CONNECTOR.ID"), index=True)
    module_params: Mapped[Optional[List["ModuleParameter"]]] = relationship()


class ModuleParameter(Base):
    __tablename__ = "MODULE_PARAMETER"
    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    key: Mapped[str] = mapped_column("KEY")
    value: Mapped[str] = mapped_column("VALUE")
    description: Mapped[str] = mapped_column("DESCRIPTION", String(500))
    created: Mapped[Optional[datetime]] = mapped_column("CREATED",
                                                        default=func.current_timestamp())
    updated: Mapped[Optional[datetime]] = mapped_column("UPDATED",
                                                        onupdate=func.current_timestamp())
    fk_moduleid: Mapped[int] = mapped_column("FK_MODULEID",
                                             ForeignKey("MODULE.ID"), index=True)


class Connector(Base):
    __tablename__ = "CONNECTOR"

    id: Mapped[int] = mapped_column("ID", SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column("NAME", String(15), nullable=False)
    status: Mapped[str] = mapped_column("STATUS", String(1), nullable=False)
    created: Mapped[Optional[datetime]] = mapped_column("CREATED",
                                                        default=func.current_timestamp())
    updated: Mapped[Optional[datetime]] = mapped_column("UPDATED",
                                                        onupdate=func.current_timestamp())
