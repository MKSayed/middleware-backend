from crud import Base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, DECIMAL


class Kiosk(Base):
    __tablename__ = "KIOSK"
    id = Column("ID", Integer, primary_key=True, index=True)
    account_no = Column("ACCOUNT_NO", DECIMAL(10), nullable=False)
    ar_name = Column("AR_NAME", String(40), nullable=False)
    eng_name = Column("ENG_NAME", String(40), nullable=False)
    descr = Column("DESCR", String(100), nullable=True)
    creation_date = Column("CREATION_DATE", DateTime, nullable=True)
    updated_date = Column("UPDATED_DATE", DateTime, nullable=True)
    status = Column("STATUS", String(1), nullable=True)
    deleted_flag = Column("DELETED_FLAG", SmallInteger, nullable=True)
    cd_part1 = Column("CD_PART1", SmallInteger, nullable=True)
    cd_part2 = Column("CD_PART2", SmallInteger, nullable=True)
    commission_check = Column("COMMISSION_CHECK", String(1), nullable=True)
    service_group_check = Column("SERVICE_GROUP_CHECK", String(1), nullable=True)
    service_charge_check = Column("SERVICE_CHARGE_CHECK", String(1), nullable=True)
    fk_service_grouno = Column("FK_SERVICE_GROUNO", SmallInteger, nullable=True)
    fk_kiosk_typeid = Column("FK_KIOSK_TYPEID", SmallInteger, nullable=True)
    fk_addressid = Column("FK_ADDRESSID", SmallInteger, nullable=True)
    fk_kiosk_familyid = Column("FK_KIOSK_FAMILYID", Integer, nullable=True)
    fk_commission_gcd = Column("FK_COMMESSION_GCD", Integer, nullable=True)

class TransactionKiosk(Base):
    __tablename__ = "TRANSACTION_KIOSK"
    number = Column("NUMBER", Integer, primary_key=True)
    name = Column("NAME", String(20), nullable=False)
    active = Column("ACTIVE", String(3), nullable=False)
    expiry_date = Column("EXPIRY_DATE", DateTime, nullable=False)
    creation_date = Column("CREATION_DATE", DateTime, nullable=False)

class KioskFamily(Base):
    __tablename__ = "KIOSK_FAMILY"
    id = Column("ID", Integer, primary_key=True, index=True)
    account_no = Column("ACCOUNT_NO", DECIMAL(10), nullable=False)
    ar_name = Column("AR_NAME", String(40), nullable=False)
    eng_name = Column("ENG_NAME", String(40), nullable=False)
    type = Column("TYPE", String(1), nullable=True)
    descr = Column("DESCR", String(100), nullable=True)
    updated_date = Column("UPDATED_DATE", DateTime, nullable=True)
    status = Column("STATUS", String(1), nullable=True)
    deleted_flag = Column("DELETED_FLAG", SmallInteger, nullable=True)
    fk_commission_gcd = Column("FK_COMMESSION_GCD", Integer, nullable=True)
    fk_service_charcd = Column("FK_SERVICE_CHARCD", Integer, nullable=True)
    fk_service_grouno = Column("FK_SERVICE_GROUNO", SmallInteger, nullable=True)
    fk_kiosk_familyid = Column("FK_KIOSK_FAMILYID", Integer, nullable=True)

class KioskOperatorLog(Base):
    __tablename__ = "KIOSK_OPERATOR_LOG"
    id = Column("ID", DECIMAL(14), primary_key=True)
    ip_address = Column("IP_ADDRESS", String(15), nullable=True)
    entrystamp = Column("ENTRYSTAMP", DateTime, nullable=True)
    aff_field = Column("AFF_FIELD", DECIMAL(10), nullable=False)
    aff_field2 = Column("AFF_FIELD2", DECIMAL(10), nullable=True)
    type = Column("TYPE", String(1), nullable=True)
    fk_kioskid = Column("FK_KIOSKID", Integer, nullable=True)

class KioskType(Base):
    __tablename__ = "KIOSK_TYPE"
    id = Column("ID", SmallInteger, primary_key=True)
    descr = Column("DESCR", String(30), nullable=False)
