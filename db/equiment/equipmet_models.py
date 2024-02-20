from crud import Base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger

class AssignedEquipment(Base):
    __tablename__ = "ASSIGNED_EQUIPMENT"
    timestamp = Column("TIMESTAMP", DateTime, primary_key=True)
    start_date = Column("START_DATE", DateTime, nullable=False)
    end_date = Column("END_DATE", DateTime, nullable=True)
    status = Column("STATUS", SmallInteger, nullable=True)
    fk_kioskid = Column("FK_KIOSKID", Integer, nullable=False)
    fk_kiosk_equipmid = Column("FK_KIOSK_EQUIPMID", Integer, nullable=False)

class EquipmentType(Base):
    __tablename__ = "EQUIPMENT_TYPE"
    cd = Column("CD", SmallInteger, primary_key=True)
    descr = Column("DESCR", String(50), nullable=True)
    status = Column("STATUS", SmallInteger, nullable=True)

class KioskEquipment(Base):
    __tablename__ = "KIOSK_EQUIPMENT"
    id = Column("ID", Integer, primary_key=True)
    descr = Column("DESCR", String(100), nullable=True)
    component_ser_num = Column("COMPONENT_SER_NUM", String(20), nullable=True)
    component_ip_address = Column("COMPONENT_IP_ADDRESS", String(15), nullable=True)
    creation_date = Column("CREATION_DATE", DateTime, nullable=True)
    status = Column("STATUS", SmallInteger, nullable=True)
    start_date = Column("START_DATE", DateTime, nullable=True)
    end_date = Column("END_DATE", DateTime, nullable=True)
    fk_equipment_tycd = Column("FK_EQUIPMENT_TYCD", SmallInteger, nullable=True)
