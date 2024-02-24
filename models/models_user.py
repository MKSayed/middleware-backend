from database import Base
from sqlalchemy import Column
from sqlalchemy import (Integer, String, SmallInteger, Date, Time, PrimaryKeyConstraint,
                        ForeignKeyConstraint, ForeignKey)
from sqlalchemy.orm import relationship

class UserType(Base):
    __tablename__ = "USER_TYPE"
    cd = Column("CD", SmallInteger, nullable=False, primary_key=True, index=True)
    descr = Column("DESCR", String(50), nullable=False)


class User(Base):
    __tablename__ = "USER"
    id = Column("ID", Integer, primary_key=True, index=True)
    username = Column("USERNAME", String(30), unique=True, nullable=False)
    password = Column("PASSWORD", String(), nullable=False)
    name = Column("NAME", String(60), nullable=False)
    national_id = Column("NATIONAL_ID", String(14), nullable=True)
    tax_id = Column("TAX_ID", Integer, nullable=True)
    fk_user_typecd = Column("FK_USER_TYPECD", SmallInteger, ForeignKey("USER_TYPE.CD"), nullable=True, index=True)
    logs = relationship("UserLog", back_populates="user")


class UserLog(Base):
    __tablename__ = "USER_LOG"
    date = Column("DATE", Date, nullable=False, index=True) 
    time = Column("TIME", Time, nullable=False, index=True)
    fk_userid = Column("FK_USERID", Integer, ForeignKey("USER.ID"), nullable=False, index=True)
    user = relationship("User", back_populates="logs")
    __table_args__ = (PrimaryKeyConstraint(date, time, fk_userid, name="idO"),)

    
class UserLogHistory(Base):
    __tablename__ = "USER_LOG_HISTORY"
    old_data = Column("OLD_DATA", String(35), nullable=False)
    fk_user_logdate = Column("FK_USER_LOGDATE", Date, nullable=False, index=True)
    fk_user_logtime = Column("FK_USER_LOGTIME", Time, nullable=False, index=True)
    fk_user_logfk_userid = Column("FK_USER_LOGFK_USERID", Integer, nullable=False, index=True)
    __table_args__ = (
    PrimaryKeyConstraint(fk_user_logdate, fk_user_logtime, fk_user_logfk_userid, name="idP"),
    ForeignKeyConstraint([fk_user_logdate, fk_user_logtime, fk_user_logfk_userid],
                                           [UserLog.date, UserLog.time, UserLog.fk_userid],))