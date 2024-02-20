from crud import Base
from sqlalchemy import Column, Integer, String, SmallInteger

class Address(Base):
    __tablename__ = "ADDRESS"
    id = Column("ID", SmallInteger, primary_key=True)
    name = Column("NAME", String(35), nullable=False)
    details = Column("DETAILS", String(65), nullable=True)
    fk_police_staticd = Column("FK_POLICE_STATICD", SmallInteger, nullable=True)
    fk_areacd = Column("FK_AREACD", Integer, nullable=True)
    fk_address_typecd = Column("FK_ADDRESS_TYPECD", SmallInteger, nullable=True)

class AddressType(Base):
    __tablename__ = "ADDRESS_TYPE"
    cd = Column("CD", SmallInteger, primary_key=True)
    descr = Column("DESCR", String(30), nullable=False)

class Area(Base):
    __tablename__ = "AREA"
    cd = Column("CD", Integer, primary_key=True)
    descr = Column("DESCR", String(20), nullable=False)

class PoliceStation(Base):
    __tablename__ = "POLICE_STATION"
    cd = Column("CD", SmallInteger, primary_key=True)
    descr = Column("DESCR", String(20), nullable=False)
