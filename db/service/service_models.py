from crud import Base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, DECIMAL

class Service(Base):
    __tablename__ = "SERVICE"
    id = Column("ID", String(5), primary_key=True)
    ar_name = Column("AR_NAME", String(40), nullable=True)
    eng_name = Column("ENG_NAME", String(40), nullable=True)
    fk_moduleser = Column("FK_MODULESER", SmallInteger, nullable=True)
    fk_serviceid = Column("FK_SERVICEID", String(5), nullable=True)
    fk_service_grouno = Column("FK_SERVICE_GROUNO", SmallInteger, nullable=True)
    fk_providerid = Column("FK_PROVIDERID", SmallInteger, nullable=True)

class ServiceCharge(Base):
    __tablename__ = "SERVICE_CHARGE"
    cd = Column("CD", Integer, primary_key=True)
    descr = Column("DESCR", String(50), nullable=False)
    value = Column("VALUE", DECIMAL(9, 2), nullable=False)
    from_value = Column("FROM", DECIMAL(9, 2), nullable=False)
    to_value = Column("TO", DECIMAL(9, 2), nullable=False)
    active_dt = Column("ACTIVE_DT", DateTime, nullable=True)
    slap = Column("SLAP", DECIMAL(9, 2), nullable=False)
    fk_commission_tcd = Column("FK_COMMESSION_TCD", SmallInteger, nullable=True)
    fk_commission_vcd = Column("FK_COMMESSION_VCD", SmallInteger, nullable=True)

class ServiceGroup(Base):
    __tablename__ = "SERVICE_GROUP"
    no = Column("NO", SmallInteger, primary_key=True)
    name = Column("NAME", String(45), nullable=False)

class ServiceParameter(Base):
    __tablename__ = "SERVICE_PARAMETER"
    ser = Column("SER", SmallInteger, primary_key=True)
    service_value = Column("SERVICE_VALUE", String(200), nullable=False)
    fk_serviceid = Column("FK_SERVICEID", String(5), nullable=False)
    fk_service_paracd = Column("FK_SERVICE_PARACD", SmallInteger, nullable=True)

class ServiceParameterType(Base):
    __tablename__ = "SERVICE_PARAMETER_TYPE"
    cd = Column("CD", SmallInteger, primary_key=True)
    descr = Column("DESCR", String(35), nullable=True)
    constancy = Column("CONSTANCY", String(1), nullable=True)
    direction = Column("DIRECTION", String(1), nullable=True)

class ServicePrice(Base):
    __tablename__ = "SERVICE_PRICE"
    id = Column("ID", SmallInteger, primary_key=True)
    stdt = Column("STDT", DateTime, nullable=False)
    enddt = Column("ENDDT", DateTime, nullable=True)
    price_value = Column("PRICE_VALUE", DECIMAL(6, 2), nullable=False)
    max_value = Column("MAX_VALUE", DECIMAL(6, 2), nullable=True)
    type = Column("TYPE", String(8), nullable=True)
    list_value = Column("LIST_VALUE", String(36), nullable=True)
    fk_serviceid = Column("FK_SERVICEID", String(5), nullable=True)
    fk_currencyid = Column("FK_CURRENCYID", SmallInteger, nullable=True)

class Provider(Base):
    __tablename__ = "PROVIDER"
    id = Column("ID", SmallInteger, primary_key=True)
    ar_name = Column("AR_NAME", String(40), nullable=False)
    eng_name = Column("ENG_NAME", String(40), nullable=False)

class PaymentType(Base):
    __tablename__ = "PAYMENT_TYPE"
    cd = Column("CD", SmallInteger, primary_key=True)
    descr = Column("DESCR", String(30), nullable=False)

class Currency(Base):
    __tablename__ = "CURRENCY"
    id = Column("ID", SmallInteger, primary_key=True)
    code = Column("CODE", String(5), nullable=False)
    name = Column("NAME", String(20), nullable=True)
    active_from = Column("ACTIVE_FROM", DateTime, nullable=True)
    rate = Column("RATE", DECIMAL(7, 2), nullable=False)
