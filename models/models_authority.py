from database import Base
from sqlalchemy import Column
from sqlalchemy import (Integer, String, SmallInteger, Date, PrimaryKeyConstraint, ForeignKey, CHAR)
from sqlalchemy.orm import relationship


class Application(Base):
    __tablename__ = 'APPLICATION'
    num = Column("NUM", SmallInteger, nullable=False, primary_key=True, index=True)
    name = Column("NAME", String(30), nullable=False)


class TransactionKiosk(Base):
    __tablename__ = "TRANSACTION_KIOSK"
    number = Column("NUMBER", Integer, nullable=False, primary_key=True, index=True)
    active = Column("ACTIVE", CHAR(3), nullable=False)
    expiry_date = Column("EXPIRY_DATE", Date, nullable=False)
    creation_date = Column("CREATION_DATE", Date, nullable=False)
    fk_applicationnum = Column("FK_APPLICATIONNUM", SmallInteger,
                               ForeignKey("APPLICATION.NUM"), index=True, nullable=True)


class Authority(Base):
    __tablename__ = "AUTHORITY"
    serial = Column("SERIAL", Integer, nullable=False)
    start_date = Column("START_DATE", Date, nullable=False)
    end_date = Column("END_DATE", Date, nullable=True)
    active = Column("ACTIVE", CHAR(1), nullable=True)
    fk_transaction_number = Column("FK_TRANSACTION_NUMBER", Integer,
                                   ForeignKey("TRANSACTION_KIOSK.NUMBER"),nullable=False, index=True)
    fk_authorized_rnumber = Column("FK_AUTHORIZED_RNUMBER", Integer,
                                   ForeignKey("AUTHORIZED_ROLE.NUMBER"), nullable=False, index=True)

    __table_args__ = (
        PrimaryKeyConstraint("FK_TRANSACTION_NUMBER", "FK_AUTHORIZED_RNUMBER"),)


class AuthorizedRole(Base):
    __tablename__ = "AUTHORIZED_ROLE"
    number = Column("NUMBER", SmallInteger, nullable=False, primary_key=True)
    name = Column("NAME", String(50), nullable=True)
    creation_date = Column("CREATION_DATE", Date, nullable=True)
    expiry_date = Column("EXPIRY_DATE", Date, nullable=True)


class AssignedRole(Base):
    __tablename__ = "ASSIGNED_ROLE"
    active = Column("ACTIVE", CHAR(1))
    creation_date = Column("CREATION_DATE", Date, nullable=False)
    fk_authorized_rnumber = Column("FK_AUTHORIZED_RNUMBER", SmallInteger,
                                   ForeignKey("AUTHORIZED_ROLE.NUMBER"),nullable=False, index=True)
    fk_userid = Column("FK_USERID", Integer, ForeignKey("USER.ID"), nullable=False, index=True)

    __table_args__ = (PrimaryKeyConstraint("FK_AUTHORIZED_RNUMBER", "FK_USERID"),)

