from crud import Base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, DECIMAL

class CommissionGroup(Base):
    __tablename__ = "COMMESSION_GROUP"
    cd = Column("CD", Integer, primary_key=True)
    descr = Column("DESCR", String(50), nullable=False)
    value = Column("VALUE", DECIMAL(9, 2), nullable=False)
    from_value = Column("FROM", DECIMAL(9, 2), nullable=False)
    to_value = Column("TO", DECIMAL(9, 2), nullable=False)
    active_dt = Column("ACTIVE_DT", DateTime, nullable=True)
    slap = Column("SLAP", DECIMAL(9, 2), nullable=False)
    fk_commission_tcd = Column("FK_COMMESSION_TCD", SmallInteger, nullable=True)
    fk_commission_vcd = Column("FK_COMMESSION_VCD", SmallInteger, nullable=True)
    fk_payment_typecd = Column("FK_PAYMENT_TYPECD", SmallInteger, nullable=True)

class CommissionType(Base):
    __tablename__ = "COMMESSION_TYPE"
    cd = Column("CD", SmallInteger, primary_key=True)
    descr = Column("DESCR", String(35), nullable=True)
    creation_date = Column("CREATION_DATE", DateTime, nullable=True)

class CommissionValueType(Base):
    __tablename__ = "COMMESSION_VALUE_TYPE"
    cd = Column("CD", SmallInteger, primary_key=True)
    descr = Column("DESCR", String(20), nullable=False)
